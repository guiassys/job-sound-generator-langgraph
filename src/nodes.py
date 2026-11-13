# src/nodes.py

import os
import yaml
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import SoundtrackState
from src.tools import generate_soundtrack_tool

# Carrega variáveis de ambiente do arquivo .env (caso existam)
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3-coder:30b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Carrega as configurações de prompts e tarefas do YAML
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "prompts.yaml")
)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)

# Instancia o modelo local via Ollama
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.2,
)


def _build_system_prompt(agent_key: str) -> str:
    """Monta a instrução de sistema (SystemMessage) a partir do YAML."""
    cfg = PROMPTS[agent_key]
    return (
        f"Papel: {cfg['role']}\n"
        f"Objetivo: {cfg['goal']}\n"
        f"Contexto e Especialidade: {cfg['backstory']}"
    )


def composer_node(state: SoundtrackState) -> dict:
    """Nó 1: Diretor Musical (Traduz o prompt do usuário em ficha técnica e slug)."""
    print("\n--- [1/3] EXECUTANDO: Diretor Musical e Arquiteto de Trilhas Sonoras ---")

    system_prompt = _build_system_prompt("composer_agent")
    user_prompt = PROMPTS["composer_agent"]["task_template"].format(
        user_prompt=state["user_prompt"]
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    musical_specification_output = response.content

    return {"musical_specification": musical_specification_output}


def sound_engineer_node(state: SoundtrackState) -> dict:
    """Nó 2: Engenheiro de Som Sênior (Gerencia VRAM e executa a síntese de áudio via MusicGen)."""
    print("\n--- [2/3] EXECUTANDO: Engenheiro de Som Sênior ---")

    system_prompt = _build_system_prompt("sound_engineer_agent")
    user_prompt = PROMPTS["sound_engineer_agent"]["task_template"].format(
        musical_specification=state["musical_specification"]
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    # Opcional: O LLM pode refinar os parâmetros antes de chamar a ferramenta física
    _ = llm.invoke(messages)

    # Executa a ferramenta local de geração de áudio (MusicGen + gestão RTX 5080)
    audio_path = generate_soundtrack_tool.invoke({
        "musical_specification": state["musical_specification"],
        "user_prompt": state["user_prompt"]
    })

    return {"audio_filepath": audio_path}


def editor_node(state: SoundtrackState) -> dict:
    """Nó 3: Editor Técnico (Compila metadados e gera o relatório final em Markdown)."""
    print("\n--- [3/3] EXECUTANDO: Editor Técnico e Documentador de Pipeline ---")

    system_prompt = _build_system_prompt("editor_agent")
    user_prompt = PROMPTS["editor_agent"]["task_template"].format(
        user_prompt=state["user_prompt"],
        musical_specification=state["musical_specification"],
        audio_filepath=state["audio_filepath"]
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    return {"final_report": response.content}