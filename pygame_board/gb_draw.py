"""Functions to draw the gameboard using Pygame."""

import os
from typing import Optional

import pygame

from pygame_board.gb_calc import (
    absolute_position_of_cell,
    height_of_inner_board,
    height_of_outer_board,
    height_of_row,
    height_of_rows,
    width_of_column,
    width_of_columns,
    width_of_inner_board,
    width_of_outer_board,
)
from pygame_board.gb_definition import Gameboard

# Cache for loaded images to avoid reloading and resizing multiple times.

image_cache: dict[str, pygame.Surface] = {}


def get_cached_image(
    _filename: str, size: Optional[tuple[int, int]] = None
) -> pygame.Surface:
    """Load and cache an image, resizing it as needed."""
    if _filename in image_cache:
        return image_cache[_filename]

    image = pygame.image.load(_filename).convert_alpha()

    if size:
        image = pygame.transform.smoothscale(image, size)

    image_cache[_filename] = image
    return image


# Drawing functions.


def draw_outer_border(gb: Gameboard, surface: pygame.Surface) -> None:
    """Draw the outer border of the gameboard."""
    pygame.draw.rect(
        surface,
        pygame.Color(gb.colour_of_outer_boarder),
        pygame.Rect(0, 0, width_of_outer_board(gb), height_of_outer_board(gb)),
    )


def draw_inner_border(gb: Gameboard, surface: pygame.Surface) -> None:
    """Draw the inner border of the gameboard."""
    pygame.draw.rect(
        surface,
        pygame.Color(gb.colour_of_inner_boarder),
        pygame.Rect(
            gb.width_of_left_outer_boarder,
            gb.height_of_top_outer_boarder,
            width_of_inner_board(gb),
            height_of_inner_board(gb),
        ),
    )


def draw_cell_area(gb: Gameboard, surface: pygame.Surface) -> None:
    """Draw the cell gutter area background."""
    pygame.draw.rect(
        surface,
        pygame.Color(gb.colour_of_cell_gutters),
        pygame.Rect(
            gb.width_of_left_outer_boarder + gb.width_of_left_inner_boarder,
            gb.height_of_top_outer_boarder + gb.height_of_top_inner_boarder,
            width_of_columns(gb),
            height_of_rows(gb),
        ),
    )


def draw_cells(gb: Gameboard, surface: pygame.Surface) -> None:
    """Draw the individual cells of the gameboard."""
    left = (
        gb.width_of_left_outer_boarder
        + gb.width_of_left_inner_boarder
        + gb.width_of_vertical_gutter[0]
    )
    top = (
        gb.height_of_top_outer_boarder
        + gb.height_of_top_inner_boarder
        + gb.height_of_horizontal_gutter[0]
    )

    for row in range(gb.number_of_cells_vertically):
        for col in range(gb.number_of_cells_horizontally):
            pygame.draw.rect(
                surface,
                pygame.Color(gb.colour_of_cell[row][col]),
                pygame.Rect(left, top, gb.width_of_cell[col], gb.height_of_cell[row]),
            )
            left += width_of_column(gb, col) + gb.width_of_vertical_gutter[col + 1]

        left = (
            gb.width_of_left_outer_boarder
            + gb.width_of_left_inner_boarder
            + gb.width_of_vertical_gutter[0]
        )
        top += height_of_row(gb, row) + gb.height_of_horizontal_gutter[row + 1]


def draw_cell_decorator(
    gb: Gameboard, surface: pygame.Surface, decorator_name: str, row: int, col: int
) -> None:
    """Draw a cell decorator image."""
    filename = os.path.join(gb.filepath, decorator_name)
    img = get_cached_image(filename, (width_of_column(gb, col), height_of_row(gb, row)))
    x, y = absolute_position_of_cell(gb, row, col)
    surface.blit(img, (x, y))


def draw_board_decorator(
    gb: Gameboard, surface: pygame.Surface, decorator_name: str, x: int, y: int
) -> None:
    """Draw a board-level decorator image."""
    filename = os.path.join(gb.filepath, decorator_name)
    img = get_cached_image(filename)
    surface.blit(img, (x, y))


def draw_gameboard(gb: Gameboard) -> pygame.Surface:
    """Draw the entire gameboard to a Pygame surface."""
    surface = pygame.Surface(
        (width_of_outer_board(gb), height_of_outer_board(gb)),
        pygame.SRCALPHA,  # pylint: disable=no-member
    )

    draw_outer_border(gb, surface)
    draw_inner_border(gb, surface)
    draw_cell_area(gb, surface)
    draw_cells(gb, surface)

    # Draw all cell decorators.

    for name, coords in gb.cell_decorators.items():
        for coord in coords:
            draw_cell_decorator(gb, surface, name, int(coord[0]), int(coord[1]))

    # Draw all board decorators.

    for name, coords in gb.board_decorators.items():
        for coord in coords:
            draw_board_decorator(gb, surface, name, int(coord[0]), int(coord[1]))

    return surface
