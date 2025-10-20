"""Function to load a Gameboard instance from a TOML configuration file."""

import os
import tomllib
from typing import Any, Dict, Tuple

from pygame_board.gb_definition import Gameboard


def load_gameboard_from_toml(_filepath: str) -> Gameboard:
    """Load a Gameboard instance from a TOML configuration file."""
    _file = os.path.join(os.getcwd(), _filepath, "_board.toml")

    with open(_file, "rb") as _file:
        _data: Dict[str, Any] = tomllib.load(_file)

    _meta = _data["meta"]
    _outer = _data["outer_boarder"]
    _inner = _data["inner_boarder"]
    _grid = _data["grid"]

    # Parse cell decorators.

    _cell_decorators: dict[str, list[Tuple[int, int]]] = {}
    for _decorator in _data.get("cell_decorator", []):
        _cell_decorators[_decorator["name"]] = [
            tuple(coord) for coord in _decorator["coords"]
        ]

    # Parse board decorators.

    _board_decorators: dict[str, list[Tuple[int, int]]] = {}
    for _decorator in _data.get("board_decorator", []):
        _board_decorators[_decorator["name"]] = [
            tuple(coord) for coord in _decorator["coords"]
        ]

    # Parse initial state.

    _initial_state: dict[str, list[Tuple[int, int]]] = {}
    for _token in _data.get("initial_state", []):
        _initial_state[_token["token"]] = [tuple(coord) for coord in _token["coords"]]

    # Instantiate the Gameboard with parsed data and return it.

    return Gameboard(
        name=_meta["name"],
        version=_meta["version"],
        date=_meta["date"],
        author=_meta["author"],
        width_of_left_outer_boarder=_outer["width_left"],
        height_of_top_outer_boarder=_outer["height_top"],
        width_of_right_outer_boarder=_outer["width_right"],
        height_of_bottom_outer_boarder=_outer["height_bottom"],
        colour_of_outer_boarder=_outer["colour"],
        width_of_left_inner_boarder=_inner["width_left"],
        height_of_top_inner_boarder=_inner["height_top"],
        width_of_right_inner_boarder=_inner["width_right"],
        height_of_bottom_inner_boarder=_inner["height_bottom"],
        colour_of_inner_boarder=_inner["colour"],
        number_of_cells_horizontally=_grid["cells_horizontal"],
        number_of_cells_vertically=_grid["cells_vertical"],
        width_of_cell=_grid["width_of_cell"],
        height_of_cell=_grid["height_of_cell"],
        colour_of_cell=_grid["colour_of_cell"],
        height_of_horizontal_gutter=_grid["horizontal_gutter"],
        width_of_vertical_gutter=_grid["vertical_gutter"],
        colour_of_cell_gutters=_grid.get("colour_of_cell_gutters", "#000000"),
        token_images=_data.get("token_images", {}),
        cell_decorators=_cell_decorators,
        board_decorators=_board_decorators,
        initial_state=_initial_state,
        filepath=_filepath,
    )
