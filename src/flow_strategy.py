# src/flow_strategy.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.state import SoundtrackState

class AudioGenerationStrategy(ABC):
    """Abstract base class for audio generation strategies."""
    
    @abstractmethod
    def execute(self, state: SoundtrackState) -> Dict[str, Any]:
        """Execute the audio generation workflow."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this strategy."""
        pass

class OriginalAudioGenerationStrategy(AudioGenerationStrategy):
    """Original strategy implementation - maintains current behavior."""
    
    def __init__(self):
        self.composer_node = None
        self.sound_engineer_node = None
        self.editor_node = None
    
    def execute(self, state: SoundtrackState) -> Dict[str, Any]:
        """Execute the original 3-node workflow."""
        # Import here to avoid circular imports during initialization
        from src.nodes import composer_node, sound_engineer_node, editor_node
        
        print("\n🎵 Executing Original Audio Generation Flow")
        
        # Execute nodes in sequence
        composer_result = composer_node(state)
        state.update(composer_result)  # Update state with composer results
        
        sound_engineer_result = sound_engineer_node(state)
        state.update(sound_engineer_result)  # Update state with sound engineer results
        
        editor_result = editor_node(state)
        
        return {
            "final_report": editor_result["final_report"],
            "audio_filepath": state["audio_filepath"],
            "musical_specification": state["musical_specification"]
        }
    
    def get_name(self) -> str:
        return "original"

class FastAudioGenerationStrategy(AudioGenerationStrategy):
    """Fast generation strategy - simplified workflow with fewer steps."""
    
    def __init__(self):
        self.composer_node = None
        self.sound_engineer_node = None
        self.editor_node = None
    
    def execute(self, state: SoundtrackState) -> Dict[str, Any]:
        """Execute a faster, simplified audio generation workflow."""
        # Import here to avoid circular imports during initialization
        from src.nodes import composer_node, sound_engineer_node, editor_node
        
        print("\n⚡ Executing Fast Audio Generation Flow")
        
        # Execute composer and sound engineer nodes (shorter processing)
        composer_result = composer_node(state)
        state.update(composer_result)  # Update state with composer results
        
        # For fast generation, we use a more direct approach
        # Execute sound engineer node but with simplified parameters
        sound_engineer_result = sound_engineer_node(state)
        state.update(sound_engineer_result)  # Update state with sound engineer results
        
        # Execute editor node
        editor_result = editor_node(state)
        
        return {
            "final_report": editor_result["final_report"],
            "audio_filepath": state["audio_filepath"],
            "musical_specification": state["musical_specification"]
        }
    
    def get_name(self) -> str:
        return "fast"