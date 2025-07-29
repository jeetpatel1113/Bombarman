import pygame
import sys
import time

# Constants
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 13, 11
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Colors
COLOR_BG = (30, 30, 30)
COLOR_GRID = (50, 50, 50)
COLOR_PLAYER = [(255, 0, 0), (0, 255, 0), (0, 128, 255), (255, 255, 0)]
COLOR_BOMB = (0, 0, 0)
COLOR_FLAME = (255, 165, 0)

# Initial game state
game_state = {
    "players": {
        "p1": {"x": 1, "y": 1, "alive": True},
        "p2": {"x": 3, "y": 5, "alive": True},
        "p3": {"x": 5, "y": 2, "alive": True},
        "p4": {"x": 9, "y": 8, "alive": True},
    },
    "bombs": [],
    "flames": []
}

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman UI + Movement")
clock = pygame.time.Clock()
spritesheet = pygame.image.load("roguelikeChar_transparent.png").convert_alpha()
SPRITE_TILE = 16
MARGIN = 1

def get_char_image(row, col):
    x = col * (SPRITE_TILE + MARGIN)
    y = row * (SPRITE_TILE + MARGIN)
    rect = pygame.Rect(x, y, SPRITE_TILE, SPRITE_TILE)
    image = spritesheet.subsurface(rect)
    # 放大为 40x40
    return pygame.transform.scale(image, (40, 40))

player_imgs = [
    get_char_image(0, 0),
    get_char_image(1, 0),
    get_char_image(2, 0),
    get_char_image(3, 0),
]

def render_game(state):
    screen.fill(COLOR_BG)

    # Draw grid
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

    # Draw flames
    for flame in state["flames"]:
        rect = pygame.Rect(flame["x"] * TILE_SIZE, flame["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_FLAME, rect)

    # Draw bombs
    for bomb in state["bombs"]:
        rect = pygame.Rect(bomb["x"] * TILE_SIZE + 10, bomb["y"] * TILE_SIZE + 10, TILE_SIZE - 20, TILE_SIZE - 20)
        pygame.draw.ellipse(screen, COLOR_BOMB, rect)

    # Draw players
    for i, (pid, pdata) in enumerate(state["players"].items()):
        if pdata["alive"]:
            px = pdata["x"] * TILE_SIZE + (TILE_SIZE - 40)//2
            py = pdata["y"] * TILE_SIZE + (TILE_SIZE - 40)//2
            screen.blit(player_imgs[i % 4], (px, py))

            if pid == "p1":
                arrow_x = px + 20 
                arrow_y = py - 8  
                pygame.draw.polygon(screen, (0, 255, 64), [
                    (arrow_x - 8, arrow_y - 8),  
                    (arrow_x + 8, arrow_y - 8),  
                    (arrow_x, arrow_y + 8)      
                ])
    pygame.display.flip()

# Main loop
last_time = time.time()
while True:
    now = time.time()
    dt = now - last_time
    last_time = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player = game_state["players"]["p1"]
            if event.key == pygame.K_w and player["y"] > 0:
                player["y"] -= 1
            elif event.key == pygame.K_s and player["y"] < GRID_HEIGHT - 1:
                player["y"] += 1
            elif event.key == pygame.K_a and player["x"] > 0:
                player["x"] -= 1
            elif event.key == pygame.K_d and player["x"] < GRID_WIDTH - 1:
                player["x"] += 1
            elif event.key == pygame.K_SPACE:
                bomb_pos = {"x": player["x"], "y": player["y"], "timer": 3}
                if bomb_pos not in game_state["bombs"]:
                    game_state["bombs"].append(bomb_pos)

    for bomb in game_state["bombs"][:]:
        bomb["timer"] -= dt
        if bomb["timer"] <= 0:

            x, y = bomb["x"], bomb["y"]
            game_state["flames"].append({"x": x, "y": y, "timer": 0.5})
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    game_state["flames"].append({"x": nx, "y": ny, "timer": 0.5})
            game_state["bombs"].remove(bomb)

    for flame in game_state["flames"][:]:
        flame["timer"] -= dt
        if flame["timer"] <= 0:
            game_state["flames"].remove(flame)

    render_game(game_state)
    clock.tick(30)
