"""Functions to manipulate tokens on the gameboard."""

import os
from typing import Dict, Tuple

import pygame

from pygame_board.gb_calc import (
    absolute_position_of_cell,
    height_of_row,
    width_of_column,
)
from pygame_board.gb_definition import Gameboard
from pygame_board.gb_draw import get_cached_image

_token_positions: Dict[Tuple[int, int], str] = {}


# Functions that actually do the drawing from the _tokens_positions dictionazry.


def draw_token(
    gb: Gameboard, surface: pygame.Surface, token: str, row: int, col: int
) -> None:
    """Draw a token."""

    # Get the filename and check to see if the tokenimage is already cached.

    filename = os.path.join(gb.filepath, gb.token_images[token])
    img = get_cached_image(filename, (width_of_column(gb, col), height_of_row(gb, row)))

    # Draw the token to the surface.

    x, y = absolute_position_of_cell(gb, row, col)
    surface.blit(img, (x, y))


def draw_tokens(gb: Gameboard, surface: pygame.Surface) -> None:
    """Draws the tokens from the _token_positions directory."""

    for _row, _col in _token_positions:
        draw_token(gb, surface, _token_positions[(_row, _col)], _row, _col)


# Functions that manipulate the _token_positions dictionary.


def place_token(token: str, row: int, col: int) -> bool:
    """Places a token into the _token_positions dictionary."""

    # Check that there is not a token already in that row and column.

    if (row, col) in _token_positions:
        return False

    # Place the token.

    _token_positions[(row, col)] = token

    return True


def move_token(from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
    """Moves a token from one row and column to another in the _token_positions dictionary."""

    # Check that there is a token in that from_row and from_column,
    # and that there isnot a token in the to_row and to_column.

    if (from_row, from_col) not in _token_positions or (
        to_row,
        to_col,
    ) in _token_positions:
        return False

    # Move the token.

    _token: str = _token_positions[(from_row, from_col)]

    del _token_positions[(from_row, from_col)]
    _token_positions[(to_row, to_col)] = _token

    return True


def remove_token(row: int, col: int) -> bool:
    """Removes a token from the _token_positions dictionary."""

    # Check that there is a token in that row and column.

    if (row, col) not in _token_positions:
        return False

    # Remove the token.

    del _token_positions[(row, col)]

    return True


def clear_tokens() -> None:
    """Clears all the tokens from the _token_positions dictionary."""

    _token_positions.clear()


def set_initial_state(gb: Gameboard, surface: pygame.Surface) -> None:
    """Sets the initial state of the tokens."""

    # Place the tokens based on the gb.initial_state.

    for _token in gb.initial_state:
        for _row, _col in gb.initial_state[_token]:
            # place_token(gb.token_images[_token], _row, _col)
            place_token(_token, _row, _col)

    # Draw the tokens.

    draw_tokens(gb, surface)
    extract_token_map(gb)


# Functions that extract the token map from the _token_positions dictionary.


def extract_token_map(gb: Gameboard) -> list[list[str]]:
    """Extracts a token map from the _token_positions dictionary"""

    _map: list[list[str]] = [[" " for _ in range(11)] for _ in range(11)]

    for _row in range(gb.number_of_cells_vertically):
        for _col in range(gb.number_of_cells_horizontally):
            if (_row, _col) in _token_positions:
                _map[_row][_col] = _token_positions[(_row, _col)]

    return _map


def print_token_map(gb: Gameboard) -> None:
    """Prints the token map."""

    _map: list[list[str]] = extract_token_map(gb)

    for _row in _map:
        print(_row, "\n")
