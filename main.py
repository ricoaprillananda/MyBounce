import pygame
import sys
import os
import random

pygame.init()

# Initialize Window
WIDTH, HEIGHT = 1368, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Bounce")

# Colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
BALL_RADIUS = 12
PADDLE_WIDTH = 160
PADDLE_HEIGHT = 15
PADDLE_SPEED = 20
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 15
SCORE_THRESHOLD = 20

# Ball Dynamics
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5

# Fullscreen Background Image Initialization
def load_background_image(filename):
    try:
        background_image = pygame.image.load(filename)
        return pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading image: {e}")
        sys.exit()

background_image = load_background_image("MyBackground.jpg")

# UI Text Styling
font = pygame.font.SysFont("Georgia", 27)


# Initialize music
def load_music(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)  #
    except pygame.error as e:
        print(f"Error loading music: {e}")
        sys.exit()

load_music("VelvetRebound.wav")

# Game Setup
score = 0
level = 1
lives = 3
high_score = 0

# Load Existing High Score
high_score_file = "My_Highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read())

# Paddle setup
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
paddle_dx = 0

# Obstacle setup
obstacles = [
    pygame.Rect(200, 300, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(400, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(600, 200, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(800, 100, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(1000, 500, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
]

# Special Features
class PowerUp:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

power_ups = [PowerUp(300, 100, 20, 20, CYAN), PowerUp(500, 150, 20, 20, MAGENTA)]

# Game Cycle Variables
clock = pygame.time.Clock()
paused = False

# Rainbow color effect for the ball
def get_rainbow_color():
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
    return random.choice(colors)

# Draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, PURPLE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Outer part
    pygame.draw.rect(screen, PINK, (x + 10, y + 5, PADDLE_WIDTH - 20, PADDLE_HEIGHT - 10))  # Inner part

# Render Obstacles
def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, get_rainbow_color(), obstacle, 0, 10)

# UI elements
def draw_ui():
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 150, 10))
    screen.blit(lives_text, (WIDTH - 150, 40))

# Main game cycle
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score when quitting
            if score > high_score:
                with open(high_score_file, "w") as f:
                    f.write(str(score))
            pygame.quit()
            sys.exit()

        # Paddle movement
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_dx = -PADDLE_SPEED
            elif event.key == pygame.K_RIGHT:
                paddle_dx = PADDLE_SPEED
            elif event.key == pygame.K_p:
                paused = not paused

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                paddle_dx = 0

    if paused:
        continue

    # Ball logic
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball Interaction with Walls
    if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
        ball_dx = -ball_dx
    if ball_y - BALL_RADIUS <= 0:
        ball_dy = -ball_dy

    # Ball Interaction with paddle
    if paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
        ball_dy = -ball_dy
        score += 1

    # Ball Interaction with obstacles
    for obstacle in obstacles:
        if obstacle.colliderect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2):
            ball_dx = -ball_dx
            score += 5  # Increase score on obstacle collision

    # Ball Interaction with power-ups
    for power_up in power_ups:
        if pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2).colliderect(power_up.rect):
            power_ups.remove(power_up)
            score += 10

    if ball_y + BALL_RADIUS > HEIGHT:
        lives -= 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 5, 5

        if lives == 0:
            if score > high_score:
                with open(high_score_file, "w") as f:
                    f.write(str(score))
            pygame.quit()
            sys.exit()

    if score >= level * SCORE_THRESHOLD:
        level += 1
        ball_dx += 2
        ball_dy += 2

    paddle_x += paddle_dx
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x + PADDLE_WIDTH > WIDTH:
        paddle_x = WIDTH - PADDLE_WIDTH

    screen.blit(background_image, (0, 0))
    pygame.draw.circle(screen, get_rainbow_color(), (ball_x, ball_y), BALL_RADIUS)
    draw_paddle(paddle_x, paddle_y)
    draw_obstacles()
    for power_up in power_ups:
        pygame.draw.rect(screen, power_up.color, power_up.rect)
    draw_ui()
    pygame.display.flip()
    clock.tick(50)
