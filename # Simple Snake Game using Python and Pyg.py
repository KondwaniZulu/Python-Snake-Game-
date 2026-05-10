
# =========================================================
# SNAKE GAME - PYTHON + PYGAME
# =========================================================
# Features:
# - Snake movement
# - Food spawning
# - Score system
# - Pause menu
# - Game over screen
# - Self collision
# - Wall collision
#
# Controls:
# Arrow Keys = Move
# P = Pause/Resume
# Q = Quit
# C = Play Again
#
# Developer Notes:
# This code is heavily commented for learning purposes.
# =========================================================

import pygame
import random

# ---------------------------------------------------------
# INITIALIZE PYGAME
# ---------------------------------------------------------
pygame.init()

# ---------------------------------------------------------
# SCREEN SETTINGS
# ---------------------------------------------------------
WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# ---------------------------------------------------------
# COLORS (RGB FORMAT)
# ---------------------------------------------------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# ---------------------------------------------------------
# GAME SETTINGS
# ---------------------------------------------------------
snake_block = 20       # Size of snake squares
snake_speed = 10       # FPS / Game speed

# Create game clock
clock = pygame.time.Clock()

# ---------------------------------------------------------
# FONTS
# ---------------------------------------------------------
font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 30)

# ---------------------------------------------------------
# FUNCTION: DISPLAY SCORE
# ---------------------------------------------------------
def show_score(score):

    # Render text
    value = score_font.render("Score: " + str(score), True, WHITE)

    # Draw text onto screen
    screen.blit(value, [10, 10])

# ---------------------------------------------------------
# FUNCTION: DRAW THE SNAKE
# ---------------------------------------------------------
def draw_snake(snake_block, snake_list):

    # Loop through every body part
    for block in snake_list:

        # Draw rectangle
        pygame.draw.rect(
            screen,
            GREEN,
            [block[0], block[1], snake_block, snake_block]
        )

# ---------------------------------------------------------
# FUNCTION: DISPLAY MESSAGE
# ---------------------------------------------------------
def message(msg, color):

    # Create text surface
    mesg = font_style.render(msg, True, color)

    # Draw text
    screen.blit(mesg, [WIDTH / 8, HEIGHT / 3])

# ---------------------------------------------------------
# FUNCTION: PAUSE MENU
# ---------------------------------------------------------
def pause_game():

    paused = True

    while paused:

        # Fill screen black
        screen.fill(BLACK)

        # Pause text
        message("PAUSED - Press P to Continue", WHITE)

        pygame.display.update()

        # Check events
        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Resume game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# ---------------------------------------------------------
# MAIN GAME FUNCTION
# ---------------------------------------------------------
def game():

    # Game states
    game_over = False
    game_close = False

    # -----------------------------------------------------
    # INITIAL SNAKE POSITION
    # -----------------------------------------------------
    x = WIDTH // 2
    y = HEIGHT // 2

    # Snake movement
    x_change = 0
    y_change = 0

    # Snake body list
    snake_list = []

    # Initial snake length
    snake_length = 1

    # -----------------------------------------------------
    # RANDOM FOOD POSITION
    # -----------------------------------------------------
    food_x = round(
        random.randrange(0, WIDTH - snake_block) / 20.0
    ) * 20

    food_y = round(
        random.randrange(0, HEIGHT - snake_block) / 20.0
    ) * 20

    # -----------------------------------------------------
    # MAIN GAME LOOP
    # -----------------------------------------------------
    while not game_over:

        # -------------------------------------------------
        # GAME OVER SCREEN LOOP
        # -------------------------------------------------
        while game_close:

            screen.fill(BLACK)

            message(
                "You Lost! Press C-Play Again or Q-Quit",
                RED
            )

            # Show final score
            show_score(snake_length - 1)

            pygame.display.update()

            # Check events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

                # Keyboard controls
                if event.type == pygame.KEYDOWN:

                    # Quit
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

                    # Restart game
                    if event.key == pygame.K_c:
                        game()

        # -------------------------------------------------
        # EVENT HANDLING
        # -------------------------------------------------
        for event in pygame.event.get():

            # Exit window
            if event.type == pygame.QUIT:
                game_over = True

            # Keyboard input
            if event.type == pygame.KEYDOWN:

                # Move LEFT
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0

                # Move RIGHT
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0

                # Move UP
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0

                # Move DOWN
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

                # Pause game
                elif event.key == pygame.K_p:
                    pause_game()

        # -------------------------------------------------
        # WALL COLLISION
        # -------------------------------------------------
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # -------------------------------------------------
        # UPDATE SNAKE POSITION
        # -------------------------------------------------
        x += x_change
        y += y_change

        # Fill background
        screen.fill(BLACK)

        # -------------------------------------------------
        # DRAW FOOD
        # -------------------------------------------------
        pygame.draw.rect(
            screen,
            RED,
            [food_x, food_y, snake_block, snake_block]
        )

        # -------------------------------------------------
        # CREATE NEW HEAD
        # -------------------------------------------------
        snake_head = []

        snake_head.append(x)
        snake_head.append(y)

        # Add head to snake body
        snake_list.append(snake_head)

        # -------------------------------------------------
        # REMOVE OLD BODY PARTS
        # -------------------------------------------------
        if len(snake_list) > snake_length:
            del snake_list[0]

        # -------------------------------------------------
        # SELF COLLISION
        # -------------------------------------------------
        for block in snake_list[:-1]:

            # If head touches body
            if block == snake_head:
                game_close = True

        # -------------------------------------------------
        # DRAW SNAKE
        # -------------------------------------------------
        draw_snake(snake_block, snake_list)

        # -------------------------------------------------
        # DISPLAY SCORE
        # -------------------------------------------------
        show_score(snake_length - 1)

        # Update screen
        pygame.display.update()

        # -------------------------------------------------
        # FOOD COLLISION
        # -------------------------------------------------
        if x == food_x and y == food_y:

            # Generate new food location
            food_x = round(
                random.randrange(0, WIDTH - snake_block) / 20.0
            ) * 20

            food_y = round(
                random.randrange(0, HEIGHT - snake_block) / 20.0
            ) * 20

            # Increase snake size
            snake_length += 1

        # -------------------------------------------------
        # CONTROL GAME SPEED
        # -------------------------------------------------
        clock.tick(snake_speed)

    # Quit pygame
    pygame.quit()

    # Exit program
    quit()

# ---------------------------------------------------------
# START GAME
# ---------------------------------------------------------
game()

