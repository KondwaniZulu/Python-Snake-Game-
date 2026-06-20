
import pygame
import random
import os

pygame.init()

# ----------------- SCREEN -----------------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Ultimate Upgrade")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ----------------- COLORS -----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (40, 40, 40)

BLUE = (0, 150, 255)
PURPLE = (180, 0, 255)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# ----------------- HIGH SCORE -----------------
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

# ----------------- HELPERS -----------------
def show_text(text, x, y, color=WHITE):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return (x, y)

def random_powerup():
    types = ["speed", "slow", "double", "poison"]
    p_type = random.choice(types)

    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

    return (x, y, p_type)

# ----------------- GAME CORE -----------------
def game():
    global high_score

    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)

    food = random_food()
    powerup = random_powerup()

    score = 0
    speed = 10

    active_effect = None
    effect_timer = 0

    running = True
    game_over = False

    while running:
        clock.tick(speed)
        screen.fill(BLACK)
        draw_grid()

        # ----------------- INPUT -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

                if game_over and event.key == pygame.K_r:
                    return game()

        # ----------------- GAME LOGIC -----------------
        if not game_over:
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # wall collision
            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_over = True

            # self collision
            if new_head in snake:
                game_over = True

            if not game_over:
                snake.insert(0, new_head)

                # food
                if new_head == food:
                    score += 1
                    food = random_food()
                    speed = 10 + score // 3
                else:
                    snake.pop()

                # power-up
                if new_head[0] == powerup[0] and new_head[1] == powerup[1]:
                    active_effect = powerup[2]
                    effect_timer = 60
                    powerup = random_powerup()

                    if active_effect == "poison":
                        game_over = True

        # ----------------- EFFECT TIMER -----------------
        if effect_timer > 0:
            effect_timer -= 1
        else:
            active_effect = None

        # apply effects
        current_speed = speed

        if active_effect == "speed":
            current_speed = 18
        elif active_effect == "slow":
            current_speed = 6

        clock.tick(current_speed)

        # ----------------- DRAW -----------------
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # power-up draw
        px, py, ptype = powerup
        color = BLUE if ptype == "speed" else PURPLE if ptype == "slow" else YELLOW if ptype == "double" else ORANGE
        pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))

        # snake
        for i, segment in enumerate(snake):
            c = GREEN if i == 0 else (0, 180, 0)
            pygame.draw.rect(screen, c, (*segment, CELL_SIZE, CELL_SIZE))

        # score logic
        display_score = score * 2 if active_effect == "double" else score

        show_text(f"Score: {display_score}", 10, 10)
        show_text(f"High Score: {high_score}", 10, 35)

        if active_effect:
            show_text(f"Effect: {active_effect}", 10, 60)

        # ----------------- GAME OVER -----------------
        if game_over:
            if display_score > high_score:
                high_score = display_score
                save_high_score(high_score)

            show_text("GAME OVER", WIDTH//2 - 80, HEIGHT//2 - 30, RED)
            show_text("Press R to Restart", WIDTH//2 - 120, HEIGHT//2)

        pygame.display.update()

    pygame.quit()

# ----------------- START SCREEN -----------------
def start_screen():
    waiting = True

    while waiting:
        screen.fill(BLACK)
        show_text("SNAKE GAME ULTIMATE", WIDTH//2 - 140, HEIGHT//2 - 60)
        show_text("Press SPACE to Start", WIDTH//2 - 130, HEIGHT//2)
        show_text("Arrow Keys to Move", WIDTH//2 - 120, HEIGHT//2 + 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
                if event.key == pygame.K_ESCAPE:
                    waiting = False

    pygame.quit()

# ----------------- RUN -----------------
start_screen()