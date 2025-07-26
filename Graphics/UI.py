import pygame
import sys

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
            rect = pygame.Rect(pdata["x"] * TILE_SIZE + 5, pdata["y"] * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
            pygame.draw.rect(screen, COLOR_PLAYER[i % 4], rect)

    pygame.display.flip()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player = game_state["players"]["p1"]
    if player["alive"]:
        if keys[pygame.K_w] and player["y"] > 0:
            player["y"] -= 1
            pygame.time.wait(100)
        elif keys[pygame.K_s] and player["y"] < GRID_HEIGHT - 1:
            player["y"] += 1
            pygame.time.wait(100)
        elif keys[pygame.K_a] and player["x"] > 0:
            player["x"] -= 1
            pygame.time.wait(100)
        elif keys[pygame.K_d] and player["x"] < GRID_WIDTH - 1:
            player["x"] += 1
            pygame.time.wait(100)
        elif keys[pygame.K_SPACE]:
            bomb_pos = {"x": player["x"], "y": player["y"], "timer": 3}
            if bomb_pos not in game_state["bombs"]:
                game_state["bombs"].append(bomb_pos)
                pygame.time.wait(200)

    render_game(game_state)
    clock.tick(30)
