# src/tools.py

import os
import re
import gc
from datetime import datetime
import torch
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from langchain_core.tools import tool


def _slugify(text: str) -> str:
    """Converte um texto livre em um slug limpo para nomes de arquivos."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:40].strip("-") or "soundtrack"


def _extract_slug(musical_specification: str, fallback_prompt: str) -> str:
    """Tenta extrair o slug sugerido na ficha técnica; caso falhe, gera a partir do prompt."""
    match = re.search(r"slug[:\s*]+([a-z0-9-]+)", musical_specification.lower())
    if match:
        return match.group(1)[:40].strip("-")
    return _slugify(fallback_prompt)


def _clear_vram():
    """Força coleta de lixo e limpeza de cache CUDA para evitar OOM na RTX 5080."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def _apply_crossfade(segments: list[AudioSegment], crossfade_ms: int = 1500) -> AudioSegment:
    """Concatena blocos de áudio aplicando crossfade suave e ajusta para 60 segundos exatos."""
    combined = segments[0]
    for seg in segments[1:]:
        combined = combined.append(seg, crossfade=crossfade_ms)

    # Garante exatamente 60.000 ms (60 segundos) com fade-out final suave
    target_duration_ms = 60_000
    if len(combined) > target_duration_ms:
        combined = combined[:target_duration_ms]
    elif len(combined) < target_duration_ms:
        silence_padding = AudioSegment.silent(duration=target_duration_ms - len(combined))
        combined = combined + silence_padding

    return combined.fade_out(2000)


@tool("generate_soundtrack_tool")
def generate_soundtrack_tool(musical_specification: str, user_prompt: str) -> str:
    """Sintetiza uma trilha sonora instrumental de 60 segundos em blocos via facebook/musicgen-large com gestão de VRAM e exporta para MP3."""
    print("🎵 [MusicGen] Iniciando síntese de áudio local...")

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = _extract_slug(musical_specification, user_prompt)
    mp3_filename = f"{timestamp}_{slug}.mp3"
    mp3_filepath = os.path.join(output_dir, mp3_filename)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "facebook/musicgen-large"

    # Limpa VRAM residual antes de carregar o modelo de áudio
    _clear_vram()

    processor = None
    model = None

    try:
        print(f"⚙️ [Hardware] Carregando '{model_id}' no dispositivo: {device.upper()}...")
        processor = AutoProcessor.from_pretrained(model_id)
        model = MusicgenForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        ).to(device)

        sampling_rate = model.config.audio_encoder.sampling_rate

        # 4 blocos progressivos (~16.5s cada, compensando os 1.5s de crossfade para fechar 60s)
        block_prompts = [
            f"Instrumental only, no vocals, ambient intro, gentle buildup: {user_prompt}",
            f"Instrumental only, no vocals, main theme development, steady rhythm: {user_prompt}",
            f"Instrumental only, no vocals, emotional climax, rich orchestration: {user_prompt}",
            f"Instrumental only, no vocals, atmospheric outro, gradual resolution: {user_prompt}",
        ]

        # ~50 tokens por segundo no MusicGen -> 825 tokens ≈ 16.5 segundos por bloco
        max_new_tokens = 825
        audio_segments = []

        for idx, prompt_text in enumerate(block_prompts, start=1):
            print(f"🎹 [Render] Sintetizando bloco {idx}/4...")
            inputs = processor(
                text=[prompt_text],
                padding=True,
                return_tensors="pt",
            ).to(device)

            with torch.no_grad():
                audio_values = model.generate(
                    **inputs,
                    do_sample=True,
                    guidance_scale=3.0,
                    max_new_tokens=max_new_tokens,
                )

            # Converte tensor para array numpy int16 e cria AudioSegment via buffer WAV temporário
            audio_np = audio_values[0, 0].cpu().float().numpy()
            audio_np = np.clip(audio_np, -1.0, 1.0)
            audio_int16 = (audio_np * 32767).astype(np.int16)

            temp_wav = os.path.join(output_dir, f"_tmp_{timestamp}_{idx}.wav")
            wavfile.write(temp_wav, rate=sampling_rate, data=audio_int16)

            segment = AudioSegment.from_wav(temp_wav)
            audio_segments.append(segment)

            # Remove WAV temporário imediatamente
            if os.path.exists(temp_wav):
                os.remove(temp_wav)

            # Libera tensores intermediários da VRAM entre os blocos
            del inputs, audio_values
            _clear_vram()

        print("🎚️ [Mixagem] Aplicando crossfade e exportando faixa final de 60s...")
        final_track = _apply_crossfade(audio_segments, crossfade_ms=1500)
        final_track.export(mp3_filepath, format="mp3", bitrate="192k")

        print(f"✅ [Concluído] Trilha salva em: {mp3_filepath}")
        return mp3_filepath

    except Exception as e:
        raise RuntimeError(f"Falha na síntese de áudio via MusicGen: {str(e)}") from e

    finally:
        # Garante liberação total da GPU ao finalizar o nó de áudio
        if model is not None:
            del model
        if processor is not None:
            del processor
        _clear_vram()