import pygame
import sys
import time
import threading
from Graphics.ui import UI  # Change to from ui import UI for single-player testing

# --- Constants ---
MAP_WIDTH = 13
MAP_HEIGHT = 11
BOMB_TIMER = 2
EXPLOSION_DURATION = 0.5
EXPLOSION_RANGE = 3

# Starting positions for each player (x, y)
START_POSITIONS = [
    (1, 1),
    (11, 1),
    (1, 9),
    (11, 9),
]

# --- Tile types ---
EMPTY = "empty"
WALL = "wall"
BLOCK = "block"
BOMB = "bomb"
EXPLOSION = "explosion"


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
    def __init__(self, start_positions=START_POSITIONS):
        self.grid = self.generate_map()
        self.players = {}
        self.bombs = []
        self.explosions = []
        self.start_positions = start_positions
        self.lock = threading.Lock()

    def add_player(self, player_id):
        if player_id <= len(self.start_positions):
            x, y = self.start_positions[player_id - 1]
            self.players[player_id] = {"pos": [x, y], "alive": True}
            print(f"Added player {player_id} at ({x}, {y}).")
        else:
            print("Error.")

    def generate_map(self):
        grid = [[EMPTY for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        center_y = MAP_HEIGHT // 2
        center_x = MAP_WIDTH // 2

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if x in (0, MAP_WIDTH - 1) or y in (0, MAP_HEIGHT - 1):
                    grid[y][x] = WALL
                elif x % 2 == 0 and y % 2 == 0:
                    grid[y][x] = WALL
                elif y == center_y or x == center_x:
                    grid[y][x] = BLOCK
                else:
                    grid[y][x] = EMPTY

        for sx, sy in [(1, 1), (1, 2), (2, 1)]:
            grid[sy][sx] = EMPTY

        return grid

    def can_move_to(self, x, y, player_id):
        if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
            return False
        if self.grid[y][x] == WALL or self.grid[y][x] == BLOCK or self.grid[y][x] == BOMB:
            return False

        for pid, player in self.players.items():
            if pid != player_id and player["alive"] and player["pos"] == [x, y]:
                return False

        return True

    def move_player(self, player_id, dx, dy):
        # Locks to ensure only one player can be on shared object (board tile)
        with self.lock:
            player = self.players[player_id]
            if not player["alive"]:
                return
            new_x = player["pos"][0] + dx
            new_y = player["pos"][1] + dy
            if self.can_move_to(new_x, new_y, player_id):
                player["pos"] = [new_x, new_y]

    def place_bomb(self, player_id):
        # Locks to ensure only one player can place bomb on shared object
        with self.lock:
            player = self.players[player_id]
            if not player["alive"]:
                return

            active_bombs = [b for b in self.bombs if not b.exploded and (b.x, b.y) == tuple(player["pos"])]
            if active_bombs:
                return

            x, y = player["pos"]
            if self.grid[y][x] == EMPTY:
                self.grid[y][x] = BOMB
                self.bombs.append(Bomb(x, y, time.time()))
                self._play_bomb = True

    def update(self):
        now = time.time()

        for bomb in self.bombs:
            if not bomb.exploded and now - bomb.placed_time >= BOMB_TIMER:
                self.explode_bomb(bomb)
                bomb.exploded = True

        self.explosions = [e for e in self.explosions if now - e.start_time < EXPLOSION_DURATION]

        for e in self.explosions:
            for x, y in e.positions:
                self.grid[y][x] = EXPLOSION

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.grid[y][x] == EXPLOSION and not any((x, y) in e.positions for e in self.explosions):
                    self.grid[y][x] = EMPTY

        for pid, player in self.players.items():
            if tuple(player["pos"]) in {pos for e in self.explosions for pos in e.positions}:
                player["alive"] = False

    def explode_bomb(self, bomb):
        self._play_explosion = True
        x, y = bomb.x, bomb.y
        affected = [(x, y)]
        self.grid[y][x] = EXPLOSION

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            for i in range(1, EXPLOSION_RANGE + 1):
                nx, ny = x + dx * i, y + dy * i
                if not (0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT):
                    break
                tile = self.grid[ny][nx]
                if tile == WALL:
                    break
                if tile == BLOCK:
                    self.grid[ny][nx] = EXPLOSION
                    affected.append((nx, ny))
                    break
                self.grid[ny][nx] = EXPLOSION
                affected.append((nx, ny))

        self.explosions.append(Explosion(affected, time.time()))

    def to_render_state(self):
        # Capture the flags
        play_bomb = getattr(self, "_play_bomb", False)
        play_explosion = getattr(self, "_play_explosion", False)

        # Now it's safe to reset
        self._play_bomb = False
        self._play_explosion = False

        walls, blocks = [], []
        for y, row in enumerate(self.grid):
            for x, t in enumerate(row):
                if t == WALL:
                    walls.append({"x": x, "y": y})
                elif t == BLOCK:
                    blocks.append({"x": x, "y": y})

        players_state = {
            f"p{pid}": {"x": p["pos"][0], "y": p["pos"][1], "alive": p["alive"]}
            for pid, p in self.players.items()
        }

        return {
            "players": players_state,
            "bombs": [{"x": b.x, "y": b.y} for b in self.bombs if not b.exploded],
            "flames": [{"x": x, "y": y} for e in self.explosions for x, y in e.positions],
            "walls": walls,
            "blocks": blocks,
            "audio": {
                "play_bomb": play_bomb,
                "play_explosion": play_explosion,
            }
        }

    @staticmethod
    def from_dict(data):
        gs = GameState()
        gs.players = {
            int(pid): {"pos": pos, "alive": alive}
            for pid, (pos, alive) in data["players"].items()
        }
        gs.bombs = [Bomb(b["x"], b["y"], b.get("placed_time", time.time()))
                    for b in data["bombs"]]
        gs.explosions = [Explosion(e["positions"], e["start_time"])
                         for e in data["explosions"]]
        gs.grid = data["grid"]
        return gs

    def to_dict(self):
        return {
            "players": {
                str(pid): (p["pos"], p["alive"]) for pid, p in self.players.items()
            },
            "bombs": [{"x": b.x, "y": b.y, "placed_time": b.placed_time}
                      for b in self.bombs],
            "explosions": [{"positions": e.positions, "start_time": e.start_time}
                           for e in self.explosions],
            "grid": self.grid
        }

    def apply_input(self, player_id, action):
        if action == "UP":
            self.move_player(player_id, 0, -1)
        elif action == "DOWN":
            self.move_player(player_id, 0, 1)
        elif action == "LEFT":
            self.move_player(player_id, -1, 0)
        elif action == "RIGHT":
            self.move_player(player_id, 1, 0)
        elif action == "BOMB":
            self.place_bomb(player_id)

    def no_explosions(self):
        if not self.explosions:
            return True
        return False


def main():
    clock = pygame.time.Clock()
    game = GameState()
    game.add_player(1)
    game_ui = UI()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # for now, control player 1
        pid = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game.apply_input(pid, "UP")
            time.sleep(0.1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game.apply_input(pid, "DOWN")
            time.sleep(0.1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.apply_input(pid, "LEFT")
            time.sleep(0.1)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.apply_input(pid, "RIGHT")
            time.sleep(0.1)
        elif keys[pygame.K_SPACE]:
            game.apply_input(pid, "BOMB")
            time.sleep(0.2)

        render_state = game.to_render_state()
        game.update()

        if render_state["audio"]["play_bomb"]:
            game_ui.play_sound("place_bomb")
        if render_state["audio"]["play_explosion"]:
            game_ui.play_sound("explosion")

        game_ui.render_game(render_state)
        clock.tick(60)


if __name__ == "__main__":
    main()
