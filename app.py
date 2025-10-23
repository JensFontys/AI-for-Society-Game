import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
LANES = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Subway Surfer - Shooter Edition (Scoring)")

# Colors
BG_COLOR = (25, 25, 25)
PLAYER_COLOR = (50, 200, 255)
RED_OBS_COLOR = (255, 60, 60)
GREEN_OBS_COLOR = (60, 255, 60)
BULLET_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Player setup
player_size = 40
player_y = HEIGHT - 120
lane_index = 1
player_rect = pygame.Rect(LANES[lane_index] - player_size // 2, player_y, player_size, player_size)

# Obstacles
obstacle_size = 40
obstacles = []  # list of tuples (rect, color, shootable)
spawn_timer = 0
spawn_interval = 80  # frames between spawns

# Bullets
bullet_size = 10
bullets = []
bullet_speed = 10
shoot_cooldown = 0

# Movement
speed = 2
background_y = 0

# Font
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

# Game variables
clock = pygame.time.Clock()
running = True
game_over = False
score = 0

def draw_text(text, y, size="normal"):
    f = big_font if size == "big" else font
    label = f.render(text, True, TEXT_COLOR)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and lane_index > 0:
                lane_index -= 1
            elif event.key == pygame.K_RIGHT and lane_index < 2:
                lane_index += 1
            elif event.key == pygame.K_SPACE and shoot_cooldown == 0:
                # Fire bullet
                bullet_x = LANES[lane_index] - bullet_size // 2
                bullet_y = player_rect.y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_size, bullet_size))
                shoot_cooldown = 15  # ~0.25s cooldown

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Restart
            obstacles.clear()
            bullets.clear()
            lane_index = 1
            player_rect.x = LANES[lane_index] - player_size // 2
            game_over = False
            score = 0

    if not game_over:
        # Smooth lane movement
        target_x = LANES[lane_index] - player_size // 2
        player_rect.x += (target_x - player_rect.x) * 0.2

        # Background scroll
        background_y += speed
        if background_y > HEIGHT:
            background_y = 0

        # Spawn new obstacles
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            lane = random.choice(LANES)
            color_choice = random.choice(["red", "green"])
            color = RED_OBS_COLOR if color_choice == "red" else GREEN_OBS_COLOR
            shootable = (color_choice == "green")
            rect = pygame.Rect(lane - obstacle_size // 2, -obstacle_size, obstacle_size, obstacle_size)
            obstacles.append((rect, color, shootable))

        # Move obstacles
        new_obstacles = []
        for rect, color, shootable in obstacles:
            rect.y += speed
            if rect.y < HEIGHT + obstacle_size:
                new_obstacles.append((rect, color, shootable))
        obstacles = new_obstacles

        # Move bullets
        for b in bullets:
            b.y -= bullet_speed
        bullets = [b for b in bullets if b.y > -bullet_size]

        # Bullet collisions (only green obstacles)
        for b in bullets[:]:
            for rect, color, shootable in obstacles[:]:
                if b.colliderect(rect):
                    if shootable:
                        bullets.remove(b)
                        obstacles.remove((rect, color, shootable))
                        score += 1  # add 1 point for each destroyed green obstacle
                    break  # stop checking once a bullet hits something

        # Player collisions
        for rect, color, shootable in obstacles:
            if player_rect.colliderect(rect):
                game_over = True
                break

        # Reduce shoot cooldown
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

    # --- Drawing ---
    screen.fill(BG_COLOR)

    # Lanes
    for x in LANES:
        pygame.draw.line(screen, (80, 80, 80), (x, 0), (x, HEIGHT), 2)

    # Obstacles
    for rect, color, shootable in obstacles:
        pygame.draw.rect(screen, color, rect)

    # Bullets
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)

    # Player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Score
    score_label = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_label, (10, 10))

    if game_over:
        draw_text("💥 GAME OVER 💥", HEIGHT // 2 - 40, size="big")
        draw_text("Press ENTER to restart", HEIGHT // 2 + 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()