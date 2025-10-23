import pygame
import random
import sys
import os

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 600
LANES = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Subway Surfer - Image Edition (no bullet image)")

# --- LOAD IMAGES ---
BASE_DIR = os.path.dirname(__file__)
assets_path = os.path.join(BASE_DIR, "assets")

player_img = pygame.image.load(os.path.join(assets_path, "player.png")).convert_alpha()
red_img = pygame.image.load(os.path.join(assets_path, "red_obstacle.png")).convert_alpha()
green_img = pygame.image.load(os.path.join(assets_path, "green_obstacle.png")).convert_alpha()
bg_img = pygame.image.load(os.path.join(assets_path, "background.png")).convert()

# Resize images to fit gameplay
player_img = pygame.transform.scale(player_img, (50, 50))
red_img = pygame.transform.scale(red_img, (40, 40))
green_img = pygame.transform.scale(green_img, (40, 40))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# --- GAME VARIABLES ---
player_y = HEIGHT - 140
lane_index = 1
player_rect = pygame.Rect(LANES[lane_index] - 25, player_y, 50, 50)

obstacles = []  # (rect, type)
bullets = []

speed = 4
bullet_speed = 10
spawn_timer = 0
spawn_interval = 70
shoot_cooldown = 0
background_y = 0
score = 0
game_over = False

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# --- HELPER FUNCTIONS ---
def draw_text_center(text, y, big=False):
    f = big_font if big else font
    label = f.render(text, True, (255, 255, 255))
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y))

# --- MAIN LOOP ---
running = True
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
                bullet_x = LANES[lane_index] - 3
                bullet_y = player_rect.y
                bullets.append(pygame.Rect(bullet_x, bullet_y, 6, 20))
                shoot_cooldown = 15

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            obstacles.clear()
            bullets.clear()
            lane_index = 1
            player_rect.x = LANES[lane_index] - 25
            score = 0
            game_over = False

    if not game_over:
        # Movement
        target_x = LANES[lane_index] - 25
        player_rect.x += (target_x - player_rect.x) * 0.2

        # Scroll background
        background_y += speed
        if background_y >= HEIGHT:
            background_y = 0

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            lane = random.choice(LANES)
            obstacle_type = random.choice(["red", "green"])
            rect = pygame.Rect(lane - 20, -40, 40, 40)
            obstacles.append((rect, obstacle_type))

        # Move obstacles
        for o in obstacles:
            o[0].y += speed
        obstacles = [o for o in obstacles if o[0].y < HEIGHT + 40]

        # Move bullets
        for b in bullets:
            b.y -= bullet_speed
        bullets = [b for b in bullets if b.y > -20]

        # Collisions
        for b in bullets[:]:
            for rect, o_type in obstacles[:]:
                if b.colliderect(rect):
                    if o_type == "green":
                        obstacles.remove((rect, o_type))
                        bullets.remove(b)
                        score += 1
                    break

        for rect, o_type in obstacles:
            if player_rect.colliderect(rect):
                game_over = True
                break

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

    # --- DRAWING ---
    # Scroll background
    screen.blit(bg_img, (0, background_y - HEIGHT))
    screen.blit(bg_img, (0, background_y))

    # Obstacles
    for rect, o_type in obstacles:
        img = green_img if o_type == "green" else red_img
        screen.blit(img, rect.topleft)

    # Bullets (draw yellow rectangles)
    for b in bullets:
        pygame.draw.rect(screen, (255, 255, 0), b)

    # Player
    screen.blit(player_img, player_rect.topleft)

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        draw_text_center("💥 GAME OVER 💥", HEIGHT // 2 - 40, big=True)
        draw_text_center("Press ENTER to restart", HEIGHT // 2 + 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
