from .imports import *
import pytest
from unittest.mock import MagicMock, patch
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

from ..funfest.tileMap import TileMap, FlyweightTile
from ..funfest.fest_message import LoopMessage, InstrumentMessage

@pytest.fixture
def setup_test_environment():
    # Create a player and position
    player = HumanPlayer("test_player")
    
    # Create a tile map with a smaller test size
    tile_map = TileMap(10, 10, 4)
    
    # Create a mock observer to track callbacks
    mock_observer = MagicMock()
    tile_map.add_observer(mock_observer)
    
    return player, tile_map, mock_observer

def test_tile_filepath_when_player_stands_on_tile(setup_test_environment):
    player, tile_map, mock_observer = setup_test_environment
    
    # Set player position to be on tile 1 (at coordinates 10,10)
    player.get_current_position = MagicMock(return_value=Coord(11, 11))
    
    # Check player position which should trigger tile activation
    tile_id, tile, sound_path = tile_map.check_player_position(player)
    
    # Verify the correct tile was detected
    assert tile_id == 1
    assert sound_path == "sound/fest/i1.wav"
    
    # Verify the observer was notified of tile activation
    mock_observer.notify_tile_activation.assert_called_once()
    args = mock_observer.notify_tile_activation.call_args[0]
    assert args[0].get_tile_id() == 1
    assert args[0].get_sound_filepath() == "sound/fest/i1.wav"
    assert args[1] == player

def test_tile_filepath_for_multiple_positions(setup_test_environment):
    player, tile_map, mock_observer = setup_test_environment
    
    # Define test cases: position and expected results
    test_positions = [
        # y, x, expected_tile_id, expected_filepath
        (11, 11, 1, "sound/fest/i1.wav"),
        (11, 15, 2, "sound/fest/i2.wav"),
        (15, 11, 5, "sound/fest/arp1.wav"),
        (15, 15, 6, "sound/fest/yeah.wav")
    ]
    
    for y, x, expected_id, expected_path in test_positions:
        mock_observer.reset_mock()
        player.get_current_position = MagicMock(return_value=Coord(y, x))
        
        # Check player position
        tile_id, tile, sound_path = tile_map.check_player_position(player)
        
        # Assert correct tile information
        assert tile_id == expected_id, f"Expected tile_id {expected_id} at ({y},{x}), got {tile_id}"
        assert sound_path == expected_path, f"Expected path {expected_path}, got {sound_path}"
        
        # Verify observer notification
        mock_observer.notify_tile_activation.assert_called_once()
        args = mock_observer.notify_tile_activation.call_args[0]
        assert args[0].get_sound_filepath() == expected_path

