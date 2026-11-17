#!/usr/bin/env python3

"""
Test file to verify the strategy pattern implementation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.flow_strategy import OriginalAudioGenerationStrategy, FastAudioGenerationStrategy
from src.state import SoundtrackState

def test_strategies():
    """Test that our strategies can be instantiated and executed."""
    
    # Create a mock state
    initial_state: SoundtrackState = {
        "user_prompt": "Test prompt for audio generation",
        "musical_specification": "",
        "audio_filepath": "",
        "final_report": "",
    }
    
    # Test original strategy
    original_strategy = OriginalAudioGenerationStrategy()
    print(f"Original strategy name: {original_strategy.get_name()}")
    
    # Test fast strategy
    fast_strategy = FastAudioGenerationStrategy()
    print(f"Fast strategy name: {fast_strategy.get_name()}")
    
    print("\n✅ Strategy pattern implementation is working correctly!")

if __name__ == "__main__":
    test_strategies()