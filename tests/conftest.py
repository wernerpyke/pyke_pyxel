import pytest
import sys
from pathlib import Path

# Add project root to path so we can import pyke_pyxel
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyke_pyxel._types import GameSettings


@pytest.fixture(autouse=True)
def reset_game_settings():
    """Reset GameSettings singleton before each test to ensure clean state."""
    # Clear the singleton instance
    GameSettings._instance = None

    # Initialize with default test values
    settings = GameSettings.get()
    settings.size.tile = 8
    settings.size.window = 160

    yield settings

    # Clean up after test
    GameSettings._instance = None
