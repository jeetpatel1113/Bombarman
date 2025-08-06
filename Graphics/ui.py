import pygame


class UI:
    # Constants
    TILE_SIZE = 40
    GRID_WIDTH, GRID_HEIGHT = 13, 11
    SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
    SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
    SPRITE_TILE = 16
    MARGIN = 1

    # Colors
    COLOR_BG = (155, 155, 155)
    COLOR_GRID = (50, 50, 50)
    COLOR_BOMB = (0, 0, 0)
    COLOR_FLAME = (255, 165, 0)
    COLOR_WALL = (50, 50, 50)
    COLOR_BLOCK = (139, 69, 19)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Bomberman UI")
        self.spritesheet = pygame.image.load("Graphics/roguelikeChar_transparent.png").convert_alpha()
        self.explosion_sound = pygame.mixer.Sound("Graphics/Audio/bomb-explosion.mp3")
        self.bomb_place_sound = pygame.mixer.Sound("Graphics/Audio/place-bomb.mp3")

        self.player_imgs = [
            self.get_char_image(0, 0),
            self.get_char_image(1, 0),
            self.get_char_image(2, 0),
            self.get_char_image(3, 0),
        ]

    def get_char_image(self, row, col):
        x = col * (self.SPRITE_TILE + self.MARGIN)
        y = row * (self.SPRITE_TILE + self.MARGIN)
        rect = pygame.Rect(x, y, self.SPRITE_TILE, self.SPRITE_TILE)
        image = self.spritesheet.subsurface(rect)

        return pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))

    def render_game(self, state):
        self.screen.fill(self.COLOR_BG)

        # Draw grid lines
        for x in range(0, self.SCREEN_WIDTH, self.TILE_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID, (x, 0), (x, self.SCREEN_HEIGHT))
        for y in range(0, self.SCREEN_HEIGHT, self.TILE_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID, (0, y), (self.SCREEN_WIDTH, y))

        # Draw flames
        for flame in state["flames"]:
            rect = pygame.Rect(flame["x"] * self.TILE_SIZE, flame["y"] * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            pygame.draw.rect(self.screen, self.COLOR_FLAME, rect)

        # Draw walls
        for wall in state.get("walls", []):
            rect = pygame.Rect(wall["x"] * self.TILE_SIZE, wall["y"] * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            pygame.draw.rect(self.screen, self.COLOR_WALL, rect)

        # Draw blocks
        for block in state.get("blocks", []):
            rect = pygame.Rect(block["x"] * self.TILE_SIZE, block["y"] * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            pygame.draw.rect(self.screen, self.COLOR_BLOCK, rect)

        # Draw bombs
        for bomb in state["bombs"]:
            rect = pygame.Rect(bomb["x"] * self.TILE_SIZE + 10, bomb["y"] * self.TILE_SIZE + 10, self.TILE_SIZE - 20,
                               self.TILE_SIZE - 20)
            pygame.draw.ellipse(self.screen, self.COLOR_BOMB, rect)

        # Draw players
        for i, (pid, pdata) in enumerate(state["players"].items()):
            if pdata["alive"]:
                px = pdata["x"] * self.TILE_SIZE + (self.TILE_SIZE - 40) // 2
                py = pdata["y"] * self.TILE_SIZE + (self.TILE_SIZE - 40) // 2
                self.screen.blit(self.player_imgs[i % len(self.player_imgs)], (px, py))

                if pid == "p1":
                    pygame.draw.polygon(self.screen, (0, 255, 64), [
                        (px + 20 - 8, py - 8),
                        (px + 20 + 8, py - 8),
                        (px + 20, py + 8)
                    ])

        pygame.display.flip()

    def play_sound(self, sound_type):
        if sound_type == "explosion":
            self.explosion_sound.play()
        elif sound_type == "place_bomb":
            self.bomb_place_sound.play()
