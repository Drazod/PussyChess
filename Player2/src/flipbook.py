# flipbook.py

import pygame
import os

# Define flip book dimensions
FLIPBOOK_WIDTH = 800  # Adjust as needed
FLIPBOOK_HEIGHT = 800  # Match the height of the screen

def display_flipbook(screen, board_width, board_height,current_page, flipbook_width=800, flipbook_height=800, background_color=(255, 255, 255), input_events=None):
    # Calculate the position of the flip book
    flipbook_x = board_width  # Place the flip book to the right of the board
    flipbook_y = 0  # Align the top of the flip book with the top of the screen

    # Directory containing images
    image_dir = r'C:\Users\Phan Thien\OneDrive\Documents\GitHub\PussyChess\Player2\assets\images'

    # Load images for the flipbook pages
    image_files = [f for f in os.listdir(image_dir) if f.startswith('page_')]
    image_files.sort()  # Ensure images are sorted in order
    pages = [pygame.image.load(os.path.join(image_dir, f)) for f in image_files]

    # Set up the flip book surface
    flipbook_screen = pygame.Surface((flipbook_width, flipbook_height))
    flipbook_screen.fill(background_color)

    # Animation parameters
    FLIP_DURATION = 10  # Duration of the flipping animation (in frames)
    flip_progress = 0    # Progress of the flipping animation (0 to FLIP_DURATION)

    # Handle input events
    if input_events:
        for event in input_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Previous page
                    if current_page > 0:
                        current_page -= 1
                        flip_progress = FLIP_DURATION  # Start flipping animation
                elif event.key == pygame.K_RIGHT:  # Next page
                    if current_page < len(pages) - 1:
                        current_page += 1
                        flip_progress = FLIP_DURATION  # Start flipping animation

    # Blit the current page onto the flip book screen
    flipbook_screen.blit(pages[current_page], (0, 0))

    # Apply flipping animation
    if flip_progress > 0:
        # Calculate the angle of rotation for the flipping animation
        flip_angle = -180 * (flip_progress / FLIP_DURATION)

        # Rotate and move the left section of the current page
        left_section_current = pygame.transform.rotate(pages[current_page].subsurface((0, 0, flipbook_width // 2, flipbook_height)), flip_angle)
        flipbook_screen.blit(left_section_current, (0, 0))

        # Rotate and move the right section of the next page
        if current_page < len(pages) - 1:
            right_section_next = pygame.transform.rotate(pages[current_page + 1].subsurface((flipbook_width // 2, 0, flipbook_width // 2, flipbook_height)), flip_angle)
            flipbook_screen.blit(right_section_next, (flipbook_width // 2, 0))

        # Decrease the progress of the flipping animation
        flip_progress -= 1

    # Return the flip book surface and current page index
    print(flipbook_screen, FLIP_DURATION, current_page)
    return flipbook_screen, FLIP_DURATION, current_page


