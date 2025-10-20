# pylint: skip-file

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Gameboard:  # pylint: disable=too-many-instance-attributes
    """A class representing a gameboard with various attributes."""

    name: str

    version: str
    date: str
    author: str

    width_of_left_outer_boarder: int
    height_of_top_outer_boarder: int
    width_of_right_outer_boarder: int
    height_of_bottom_outer_boarder: int
    colour_of_outer_boarder: str

    width_of_left_inner_boarder: int
    height_of_top_inner_boarder: int
    width_of_right_inner_boarder: int
    height_of_bottom_inner_boarder: int
    colour_of_inner_boarder: str

    number_of_cells_horizontally: int
    number_of_cells_vertically: int
    width_of_cell: List[int]
    height_of_cell: List[int]
    colour_of_cell: List[List[str]]

    height_of_horizontal_gutter: List[int]
    width_of_vertical_gutter: List[int]
    colour_of_cell_gutters: str

    token_images: Dict[str, str]
    cell_decorators: Dict[str, List[Tuple[int, int]]]
    board_decorators: Dict[str, List[Tuple[int, int]]]

    initial_state: dict[str, list[Tuple[int, int]]]

    filepath: str
