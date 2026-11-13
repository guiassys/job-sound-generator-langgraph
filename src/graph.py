# src/graph.py

from langgraph.graph import StateGraph, START, END
from src.state import SoundtrackState
from src.nodes import composer_node, sound_engineer_node, editor_node


def create_workflow():
    """Constrói e compila o grafo de estados do pipeline Job Sound Generator."""
    # Inicializa o grafo tipado com o contrato de estado compartilhado
    workflow = StateGraph(SoundtrackState)

    # Registra os nós (etapas do pipeline)
    workflow.add_node("composer_agent", composer_node)
    workflow.add_node("sound_engineer_agent", sound_engineer_node)
    workflow.add_node("editor_agent", editor_node)

    # Define o fluxo sequencial (arestas)
    workflow.add_edge(START, "composer_agent")
    workflow.add_edge("composer_agent", "sound_engineer_agent")
    workflow.add_edge("sound_engineer_agent", "editor_agent")
    workflow.add_edge("editor_agent", END)

    # Compila o grafo para execução
    return workflow.compile()