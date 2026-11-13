# src/state.py

from typing import TypedDict


class SoundtrackState(TypedDict):
    """Contrato de estado compartilhado entre os nós do pipeline Job Sound Generator."""

    user_prompt: str
    musical_specification: str
    audio_filepath: str
    final_report: str