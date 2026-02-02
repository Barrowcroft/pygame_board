"""Test script for pygame_board."""

## Because pygame has no stub files.
# pylint: disable=no-member, no-name-in-module
# pyright: reportUnknownMemberType=false
# pyright: reportAttributeAccessIssue=false

# Because we want them:
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

import pygame

from pygame_board.gb_calc import total_board_size
from pygame_board.gb_draw import draw_gameboard
from pygame_board.gb_loader import load_gameboard_from_toml
from pygame_board.gb_tokens import (
    clear_tokens,
    draw_tokens,
    print_token_map,
    set_initial_state,
)

# Load the gameboard.

gb = load_gameboard_from_toml("pygame_board/saves/hnefatafl")
gb_size = total_board_size(gb)


# Create a window.

pygame.init()
screen = pygame.display.set_mode(gb_size)
pygame.display.set_caption("Minimal Pygame")

# Draw the gameboard.

gb_surface = draw_gameboard(gb)
set_initial_state(gb, screen)

# Main loop
_running: bool = True

while _running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                clear_tokens()
            if event.key == pygame.K_s:
                set_initial_state(gb, screen)
            if event.key == pygame.K_m:
                print_token_map(gb)

    # Render the board.
    screen.blit(gb_surface, (0, 0))
    draw_tokens(gb, screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
