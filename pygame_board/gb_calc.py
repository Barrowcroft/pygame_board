"""Functions to calculate dimensions of the gameboard,
and to find the row and column of a cell at given absolute coordinates,
and to find the absolute coordinates of a cell at given row and column."""

from typing import Tuple

from pygame_board.gb_definition import Gameboard


def height_of_row(gb: Gameboard, row: int) -> int:
    """Calculate the total height of a specified row in the gameboard."""
    return gb.height_of_cell[row]


def height_of_rows(gb: Gameboard) -> int:
    """Calculate the total height of all rows in the gameboard."""
    _height: int = 0
    for _row in range(gb.number_of_cells_vertically):
        _height += height_of_row(gb, _row)
    for _row in range(gb.number_of_cells_vertically + 1):
        _height += gb.height_of_horizontal_gutter[_row]
    return _height


def height_of_inner_board(gb: Gameboard) -> int:
    """Calculate the total height of the inner board of the gameboard."""
    return (
        gb.height_of_top_inner_boarder
        + height_of_rows(gb)
        + gb.height_of_bottom_inner_boarder
    )


def height_of_outer_board(gb: Gameboard) -> int:
    """Calculate the total height of the outer board of the gameboard."""
    return (
        gb.height_of_top_outer_boarder
        + height_of_inner_board(gb)
        + gb.height_of_bottom_outer_boarder
    )


def width_of_column(gb: Gameboard, column: int) -> int:
    """Calculate the total width of a specified column in the gameboard."""
    return gb.width_of_cell[column]


def width_of_columns(gb: Gameboard) -> int:
    """Calculate the total width of all columns in the gameboard."""
    _width: int = 0
    for _column in range(gb.number_of_cells_horizontally):
        _width += width_of_column(gb, _column)
    for _column in range(gb.number_of_cells_horizontally + 1):
        _width += gb.width_of_vertical_gutter[_column]
    return _width


def width_of_inner_board(gb: Gameboard) -> int:
    """Calculate the total width of the inner board of the gameboard."""
    return (
        gb.width_of_left_inner_boarder
        + width_of_columns(gb)
        + gb.width_of_right_inner_boarder
    )


def width_of_outer_board(gb: Gameboard) -> int:
    """Calculate the total width of the outer board of the gameboard."""
    return (
        gb.width_of_left_outer_boarder
        + width_of_inner_board(gb)
        + gb.width_of_right_outer_boarder
    )


def total_board_size(gb: Gameboard) -> Tuple[int, int]:
    """Returns the total size of the gameboard."""
    return width_of_outer_board(gb), height_of_outer_board(gb)


def absolute_position_of_cell(gb: Gameboard, row: int, col: int) -> tuple[int, int]:
    """Calculate the absolute position (top-left corner) of a specified cell."""
    _x: int = gb.width_of_left_outer_boarder + gb.width_of_left_inner_boarder
    _y: int = gb.height_of_top_outer_boarder + gb.height_of_top_inner_boarder

    for _col in range(col):
        _x += gb.width_of_cell[_col] + gb.width_of_vertical_gutter[_col + 1]

    for _row in range(row):
        _y += gb.height_of_cell[_row] + gb.height_of_horizontal_gutter[_row + 1]

    _x += gb.width_of_vertical_gutter[0]
    _y += gb.height_of_horizontal_gutter[0]

    return (_x, _y)


def cell_at_absolute_coordinates(
    gb: Gameboard, x: int, y: int
) -> tuple[int, int] | None:
    """Determine the cell (row, column) at a given absolute position (x, y)."""
    current_x = (
        gb.width_of_left_outer_boarder
        + gb.width_of_left_inner_boarder
        + gb.width_of_vertical_gutter[0]
    )
    current_y = (
        gb.height_of_top_outer_boarder
        + gb.height_of_top_inner_boarder
        + gb.height_of_horizontal_gutter[0]
    )

    for col in range(gb.number_of_cells_horizontally):
        cell_width = gb.width_of_cell[col]
        if current_x <= x < current_x + cell_width:
            for row in range(gb.number_of_cells_vertically):
                cell_height = gb.height_of_cell[row]
                if current_y <= y < current_y + cell_height:
                    return (row, col)
                current_y += cell_height + gb.height_of_horizontal_gutter[row + 1]
            return None
        current_x += cell_width + gb.width_of_vertical_gutter[col + 1]
        current_y = (
            gb.height_of_top_outer_boarder
            + gb.height_of_top_inner_boarder
            + gb.height_of_horizontal_gutter[0]
        )

    return None
