# main.py

import os
from datetime import datetime
from dotenv import load_dotenv
from src.graph import create_workflow

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "output")),
)
DEFAULT_PROMPT = os.getenv(
    "USER_PROMPT",
    "Epic orchestral cinematic soundtrack for a medieval fantasy game adventure, heroic brass and driving strings",
)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    user_prompt = DEFAULT_PROMPT
    if not user_prompt:
        user_prompt = input("Digite o prompt descritivo para a trilha sonora: ")

    print("## Iniciando Pipeline Job Sound Generator (LangGraph + Ollama + MusicGen) ##")
    print(f"Prompt: {user_prompt}\n")

    # Estado inicial injetado no grafo
    initial_state = {
        "user_prompt": user_prompt,
        "musical_specification": "",
        "audio_filepath": "",
        "final_report": "",
    }

    # Compila e executa o pipeline
    app = create_workflow()
    resultado_final = app.invoke(initial_state)

    final_content = resultado_final.get(
        "final_report", "Nenhum relatório foi gerado pela pipeline."
    )
    audio_filepath = resultado_final.get("audio_filepath", "")

    # Deriva o nome do arquivo markdown usando o mesmo timestamp/slug do áudio gerado, se disponível
    if audio_filepath and os.path.exists(audio_filepath):
        base_name = os.path.splitext(os.path.basename(audio_filepath))[0]
        markdown_filename = f"{base_name}.md"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        markdown_filename = f"{timestamp}_soundtrack.md"

    filepath = os.path.join(OUTPUT_DIR, markdown_filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(final_content))

    print("\n\n##################################################")
    print(f"## RELATÓRIO SALVO COM SUCESSO: {filepath} ##")
    if audio_filepath:
        print(f"## ÁUDIO GERADO: {audio_filepath} ##")
    print("##################################################\n")
    print(final_content)


if __name__ == "__main__":
    main()