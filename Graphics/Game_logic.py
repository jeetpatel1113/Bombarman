import time
import pygame
import sys

TILE_SIZE = 32
MAP_WIDTH = 15
MAP_HEIGHT = 15
BOMB_TIMER = 2
EXPLOSION_DURATION = 0.5
EXPLOSION_RANGE = 5

# --- Tile types ---
EMPTY = "empty"
WALL = "wall"
BLOCK = "block"
BOMB = "bomb"
EXPLOSION = "explosion"
PLAYER = "player"

# Will be replaced with UI later
COLOR_MAP = {
    EMPTY: (200, 200, 200),
    WALL: (50, 50, 50),
    BLOCK: (139, 69, 19),
    BOMB: (0, 0, 0),
    EXPLOSION: (255, 140, 0),
    PLAYER: (0, 0, 255),
}


class Bomb:
    def __init__(self, x, y, placed_time):
        self.x = x
        self.y = y
        self.placed_time = placed_time
        self.exploded = False


class Explosion:
    def __init__(self, positions, start_time):
        self.positions = positions
        self.start_time = start_time


class GameState:
    def __init__(self):
        self.grid = self.generate_map()
        self.player_pos = [1, 1]
        self.bombs = []
        self.explosions = []

    def generate_map(self):
        grid = [[EMPTY for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if x == 0 or y == 0 or x == MAP_WIDTH - 1 or y == MAP_HEIGHT - 1:
                    grid[y][x] = WALL
                elif x % 2 == 0 and y % 2 == 0:
                    grid[y][x] = WALL
                elif (x, y) not in [(1, 1), (1, 2), (2, 1)]:
                    grid[y][x] = BLOCK

        return grid

    def can_move_to(self, x, y):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.grid[y][x] in [EMPTY]
        return False

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if self.can_move_to(new_x, new_y):
            self.player_pos = [new_x, new_y]

    def place_bomb(self):
        x, y = self.player_pos
        if self.grid[y][x] == EMPTY:
            self.grid[y][x] = BOMB
            self.bombs.append(Bomb(x, y, time.time()))

    def update(self):
        now = time.time()

        # Handle bomb explosions
        for bomb in self.bombs:
            if not bomb.exploded and now - bomb.placed_time >= BOMB_TIMER:
                self.explode_bomb(bomb)
                bomb.exploded = True

        # Remove expired explosions
        self.explosions = [e for e in self.explosions if now - e.start_time < EXPLOSION_DURATION]
        for e in self.explosions:
            for x, y in e.positions:
                self.grid[y][x] = EXPLOSION

        # Clear old explosions
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.grid[y][x] == EXPLOSION:
                    if not any((x, y) in e.positions for e in self.explosions):
                        self.grid[y][x] = EMPTY

    def explode_bomb(self, bomb):
        x, y = bomb.x, bomb.y
        self.grid[y][x] = EXPLOSION
        affected = [(x, y)]

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, EXPLOSION_RANGE + 1):
                nx, ny = x + dx * i, y + dy * i
                if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                    break
                tile = self.grid[ny][nx]
                if tile == WALL:
                    break
                elif tile == BLOCK:
                    self.grid[ny][nx] = EXPLOSION
                    affected.append((nx, ny))
                    break
                else:
                    self.grid[ny][nx] = EXPLOSION
                    affected.append((nx, ny))

        self.explosions.append(Explosion(affected, time.time()))
        self.grid[y][x] = EXPLOSION


def main():
    print("Arrows to move and Space to place bomb!")
    pygame.init()
    screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
    pygame.display.set_caption("Single Player Bomberman")
    clock = pygame.time.Clock()

    game = GameState()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.move_player(0, -1)
            time.sleep(0.1)
        elif keys[pygame.K_DOWN]:
            game.move_player(0, 1)
            time.sleep(0.1)
        elif keys[pygame.K_LEFT]:
            game.move_player(-1, 0)
            time.sleep(0.1)
        elif keys[pygame.K_RIGHT]:
            game.move_player(1, 0)
            time.sleep(0.1)
        elif keys[pygame.K_SPACE]:
            game.place_bomb()
            time.sleep(0.2)

        game.update()

        # Draw
        screen.fill((0, 0, 0))
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile = game.grid[y][x]
                color = COLOR_MAP.get(tile, (255, 255, 255))
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, color, rect)

        # Draw player
        px, py = game.player_pos
        rect = pygame.Rect(px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_MAP[PLAYER], rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
