import pygame

# Constants
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 13, 11
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Colors
COLOR_BG = (155, 155, 155)
COLOR_GRID = (50, 50, 50)
COLOR_BOMB = (0, 0, 0)
COLOR_FLAME = (255, 165, 0)
COLOR_WALL = (50, 50, 50)
COLOR_BLOCK = (139, 69, 19)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman UI")
spritesheet = pygame.image.load("graphics/roguelikeChar_transparent.png").convert_alpha()
SPRITE_TILE = 16
MARGIN = 1

def get_char_image(row, col):
    x = col * (SPRITE_TILE + MARGIN)
    y = row * (SPRITE_TILE + MARGIN)
    rect = pygame.Rect(x, y, SPRITE_TILE, SPRITE_TILE)
    image = spritesheet.subsurface(rect)
    # 放大为 40x40
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

player_imgs = [
    get_char_image(0, 0),
    get_char_image(1, 0),
    get_char_image(2, 0),
    get_char_image(3, 0),
]

def render_game(state):
    screen.fill(COLOR_BG)

    # Draw grid lines
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

    # Draw flames
    for flame in state["flames"]:
        rect = pygame.Rect(flame["x"] * TILE_SIZE, flame["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_FLAME, rect)

    # Draw walls
    for wall in state.get("walls", []):
        rect = pygame.Rect(wall["x"] * TILE_SIZE, wall["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_WALL, rect)

    # Draw blocks
    for block in state.get("blocks", []):
        rect = pygame.Rect(block["x"] * TILE_SIZE, block["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_BLOCK, rect)

    # Draw bombs
    for bomb in state["bombs"]:
        rect = pygame.Rect(bomb["x"] * TILE_SIZE + 10, bomb["y"] * TILE_SIZE + 10, TILE_SIZE - 20, TILE_SIZE - 20)
        pygame.draw.ellipse(screen, COLOR_BOMB, rect)

    # Draw players
    for i, (pid, pdata) in enumerate(state["players"].items()):
        if pdata["alive"]:
            px = pdata["x"] * TILE_SIZE + (TILE_SIZE - 40)//2
            py = pdata["y"] * TILE_SIZE + (TILE_SIZE - 40)//2
            screen.blit(player_imgs[i % len(player_imgs)], (px, py))

            if pid == "p1":
                pygame.draw.polygon(screen, (0, 255, 64), [
                    (px + 20 - 8, py - 8),
                    (px + 20 + 8, py - 8),
                    (px + 20, py + 8)
                ])

    pygame.display.flip()
