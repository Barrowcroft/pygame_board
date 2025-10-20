"""Test script for pygame_board."""

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

pygame.init()  # pylint: disable=no-member
screen = pygame.display.set_mode(gb_size)
pygame.display.set_caption("Minimal Pygame")

# Draw the gameboard.

gb_surface = draw_gameboard(gb)
set_initial_state(gb, screen)

# Main loop
_running: bool = True

while _running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            _running = False  # pylint: disable=invalid-name
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key == pygame.K_d:  # pylint: disable=no-member
                clear_tokens()
            if event.key == pygame.K_s:  # pylint: disable=no-member
                set_initial_state(gb, screen)
            if event.key == pygame.K_m:  # pylint: disable=no-member
                print_token_map(gb)

    # Render the board.
    screen.blit(gb_surface, (0, 0))
    draw_tokens(gb, screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()  # pylint: disable=no-member
