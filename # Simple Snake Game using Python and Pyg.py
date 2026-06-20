
import pygame
import random
import os

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Ultimate Boss Edition")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# ---------------- COLORS ----------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 50, 50)
GRAY = (80, 80, 80)

BLUE = (0, 150, 255)
PURPLE = (180, 0, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
DARK_RED = (150, 0, 0)

# ---------------- HIGH SCORE ----------------
FILE = "highscore.txt"

def load_score():
    if os.path.exists(FILE):
        return int(open(FILE).read())
    return 0

def save_score(s):
    open(FILE, "w").write(str(s))

high_score = load_score()

# ---------------- HELPERS ----------------
def draw_text(text, x, y, c=(255,255,255)):
    screen.blit(font.render(text, True, c), (x, y))

def rand_food(snake, obs):
    while True:
        x = random.randint(0, (WIDTH//CELL)-1)*CELL
        y = random.randint(0, (HEIGHT//CELL)-1)*CELL
        if (x,y) not in snake and (x,y) not in obs:
            return (x,y)

def rand_power():
    types = ["speed","slow","double","poison"]
    t = random.choice(types)
    x = random.randint(0,(WIDTH//CELL)-1)*CELL
    y = random.randint(0,(HEIGHT//CELL)-1)*CELL
    return (x,y,t)

def gen_obstacles(level):
    obs = set()
    for _ in range(5 + level*2):
        x = random.randint(0,(WIDTH//CELL)-1)*CELL
        y = random.randint(0,(HEIGHT//CELL)-1)*CELL
        obs.add((x,y))
    return obs

# ---------------- BOSS SYSTEM ----------------
class Boss:
    def __init__(self):
        self.x = WIDTH//2
        self.y = 0
        self.dir = 1
        self.hp = 10

    def move(self):
        self.x += self.dir * CELL
        if self.x <= 0 or self.x >= WIDTH-CELL:
            self.dir *= -1
            self.y += CELL

    def draw(self):
        pygame.draw.rect(screen, DARK_RED, (self.x, self.y, CELL*2, CELL*2))
        draw_text(f"BOSS HP: {self.hp}", 350, 10, RED)

    def collide(self, snake_head):
        bx = (self.x, self.y)
        return snake_head == bx or snake_head == (self.x+CELL, self.y)

# ---------------- GAME ----------------
def game():
    global high_score

    snake = [(100,100)]
    direction = (CELL,0)

    score = 0
    level = 1
    speed = 10

    obstacles = gen_obstacles(level)

    food = rand_food(snake, obstacles)
    power = rand_power()

    boss = None
    boss_active = False

    effect = None
    timer = 0

    running = True
    game_over = False

    while running:
        screen.fill(BLACK)
        clock.tick(speed)

        # ---------------- INPUT ----------------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction!=(0,CELL):
                    direction=(0,-CELL)
                if e.key == pygame.K_DOWN and direction!=(0,-CELL):
                    direction=(0,CELL)
                if e.key == pygame.K_LEFT and direction!=(CELL,0):
                    direction=(-CELL,0)
                if e.key == pygame.K_RIGHT and direction!=(-CELL,0):
                    direction=(CELL,0)

                if game_over and e.key == pygame.K_r:
                    return game()

        # ---------------- LEVEL SYSTEM ----------------
        if score > 0 and score % 5 == 0:
            level += 1
            obstacles |= gen_obstacles(level)
            speed = min(20, speed+1)

        # ---------------- BOSS LEVEL ----------------
        if level % 3 == 0:
            if boss is None:
                boss = Boss()
                boss_active = True

        # ---------------- GAME LOGIC ----------------
        if not game_over:
            head = snake[0]
            new_head = (head[0]+direction[0], head[1]+direction[1])

            if (new_head[0]<0 or new_head[0]>=WIDTH or
                new_head[1]<0 or new_head[1]>=HEIGHT):
                game_over=True

            if new_head in snake or new_head in obstacles:
                game_over=True

            if boss_active and boss:
                if boss.collide(new_head):
                    game_over=True

            if not game_over:
                snake.insert(0,new_head)

                if new_head == food:
                    score+=1
                    food=rand_food(snake,obstacles)

                else:
                    snake.pop()

                # power
                if new_head == (power[0],power[1]):
                    effect = power[2]
                    timer = 50
                    power = rand_power()

                    if effect=="poison":
                        game_over=True

        # ---------------- BOSS MOVEMENT ----------------
        if boss_active and boss:
            boss.move()
            boss.draw()

            if snake[0][0] == boss.x and snake[0][1] == boss.y:
                boss.hp -= 1

            if boss.hp <= 0:
                boss_active=False
                boss=None

        # ---------------- EFFECTS ----------------
        if timer>0:
            timer-=1
        else:
            effect=None

        sp = speed
        if effect=="speed":
            sp=18
        if effect=="slow":
            sp=6

        clock.tick(sp)

        # ---------------- DRAW ----------------
        for o in obstacles:
            pygame.draw.rect(screen, GRAY, (*o,CELL,CELL))

        pygame.draw.rect(screen, RED, (*food,CELL,CELL))

        px,py,pt=power
        c = BLUE if pt=="speed" else PURPLE if pt=="slow" else YELLOW if pt=="double" else ORANGE
        pygame.draw.rect(screen,c,(px,py,CELL,CELL))

        for i,s in enumerate(snake):
            pygame.draw.rect(screen, GREEN if i==0 else DARK_GREEN, (*s,CELL,CELL))

        draw_text(f"Score: {score}",10,10)
        draw_text(f"Level: {level}",10,35)
        draw_text(f"High: {high_score}",10,60)

        if boss_active:
            draw_text("BOSS LEVEL!", 250, 10, RED)

        if game_over:
            if score>high_score:
                high_score=score
                save_score(high_score)

            draw_text("GAME OVER",220,180,RED)
            draw_text("Press R",240,210,RED)

        pygame.display.update()

    pygame.quit()

# ---------------- START ----------------
def start():
    run=True
    while run:
        screen.fill(BLACK)
        draw_text("SNAKE ULTIMATE ARCADE",160,150)
        draw_text("SPACE TO START",200,190)
        draw_text("BOSS LEVELS ENABLED",180,220,RED)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    game()
                if e.key==pygame.K_ESCAPE:
                    run=False

    pygame.quit()

start()