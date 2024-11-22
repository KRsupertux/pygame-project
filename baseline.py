import pygame
import math
import sys
import random

class Engine:
    def __init__(self, map_file, tile_size, player_size, player_speed, run_speed_multiplier):
        self.TILE_SIZE = tile_size
        self.MAP_WIDTH = 0
        self.MAP_HEIGHT = 0
        self.player_size = player_size
        self.player_pos = [0, 0]
        self.player_velocity = [0, 0]
        self.player_speed = player_speed
        self.run_speed_multiplier = run_speed_multiplier
        self.map_layout = self.load_map(map_file)

    def load_map(self, map_file):
        layout = []
        with open(map_file, 'r') as file:
            rows = file.readlines()

        # Create map layout from file data
        for row in rows:
            row_data = []
            for tile in row.strip():
                if tile == '0':
                    row_data.append(0)  # Grass
                elif tile == '1':
                    row_data.append(1)  # Dirt
                elif tile == '2':
                    row_data.append(2)  # Water
                elif tile == '3':
                    row_data.append(3)  # Rock (impassable)
                elif tile == '4':
                    row_data.append(4)  # Road
                elif tile == '5':
                    row_data.append(5)  # River
            layout.append(row_data)

        # Set map size based on loaded data
        self.MAP_ROWS = len(layout)
        self.MAP_COLS = len(layout[0])
        self.MAP_WIDTH = self.MAP_COLS * self.TILE_SIZE
        self.MAP_HEIGHT = self.MAP_ROWS * self.TILE_SIZE
        self.player_pos = [self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2]
        return layout

    def handle_movement(self, keys):
        self.player_velocity = [0, 0]
        player_tile_x = self.player_pos[0] // self.TILE_SIZE
        player_tile_y = self.player_pos[1] // self.TILE_SIZE

        if keys[pygame.K_UP] and not self.is_obstacle(player_tile_x, player_tile_y - 0.2):
            self.player_velocity[1] -= self.player_speed
        if keys[pygame.K_DOWN] and not self.is_obstacle(player_tile_x, player_tile_y + 0.2):
            self.player_velocity[1] += self.player_speed
        if keys[pygame.K_LEFT] and not self.is_obstacle(player_tile_x - 0.2, player_tile_y):
            self.player_velocity[0] -= self.player_speed
        if keys[pygame.K_RIGHT] and not self.is_obstacle(player_tile_x + 0.2, player_tile_y):
            self.player_velocity[0] += self.player_speed

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player_velocity[0] *= self.run_speed_multiplier
            self.player_velocity[1] *= self.run_speed_multiplier

    def is_obstacle(self, tile_x, tile_y):
        if 0 <= tile_x < self.MAP_COLS and 0 <= tile_y < self.MAP_ROWS:
            return self.map_layout[math.floor(tile_y)][math.floor(tile_x)] == 3
        return True

    def update_player_position(self):
        self.player_pos[0] += self.player_velocity[0]
        self.player_pos[1] += self.player_velocity[1]
        self.player_pos[0] = max(0, min(self.player_pos[0], self.MAP_WIDTH - self.player_size))
        self.player_pos[1] = max(0, min(self.player_pos[1], self.MAP_HEIGHT - self.player_size))


class Display:
    def __init__(self, engine, screen_width, screen_height, fps):
        self.engine = engine
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Realistic Map with Impassable Obstacles")
        self.clock = pygame.time.Clock()
        self.FPS = fps

        self.textures = self.load_textures()
        self.player_color = (0, 0, 255)

    def load_textures(self):
        textures = {}
        textures[0] = self.create_texture((50, 150, 50))  # Grass
        textures[1] = self.create_texture((139, 69, 19))  # Dirt
        textures[3] = self.create_texture((200, 50, 50))  # Rock (impassable)
        textures[4] = self.create_texture((100, 100, 100))  # Road
        textures[5] = self.create_texture((173, 216, 230))  # Water
        return textures

    @staticmethod
    def create_texture(color):
        surface = pygame.Surface((50, 50))
        surface.fill(color)
        return surface

    def draw_map(self, offset_x, offset_y):
        for row in range(self.engine.MAP_ROWS):
            for col in range(self.engine.MAP_COLS):
                tile_x = col * self.engine.TILE_SIZE + offset_x
                tile_y = row * self.engine.TILE_SIZE + offset_y
                if tile_x + self.engine.TILE_SIZE < 0 or tile_y + self.engine.TILE_SIZE < 0 or tile_x > self.SCREEN_WIDTH or tile_y > self.SCREEN_HEIGHT:
                    continue
                tile_type = self.engine.map_layout[row][col]
                if tile_type in self.textures:
                    self.screen.blit(self.textures[tile_type], (tile_x, tile_y))

    def draw_player(self, offset_x, offset_y):
        pygame.draw.rect(
            self.screen,
            self.player_color,
            (self.SCREEN_WIDTH // 2 - self.engine.player_size // 2,
             self.SCREEN_HEIGHT // 2 - self.engine.player_size // 2,
             self.engine.player_size, self.engine.player_size)
        )

    def draw_minimap(self):
        minimap_width = 200
        minimap_height = 150
        minimap_tile_size = 25  # Number of tiles in the minimap

        player_tile_x = self.engine.player_pos[0] / self.engine.TILE_SIZE
        player_tile_y = self.engine.player_pos[1] / self.engine.TILE_SIZE

        minimap_center_x = player_tile_x
        minimap_center_y = player_tile_y

        minimap_start_x = max(0, minimap_center_x - minimap_tile_size / 2)
        minimap_start_y = max(0, minimap_center_y - minimap_tile_size / 2)

        minimap_end_x = minimap_start_x + minimap_tile_size
        minimap_end_y = minimap_start_y + minimap_tile_size

        minimap_surface = pygame.Surface((minimap_width, minimap_height))
        minimap_surface.fill((100, 100, 100))

        tile_scale_x = minimap_width / minimap_tile_size
        tile_scale_y = minimap_height / minimap_tile_size

        for y in range(int(minimap_start_y), int(minimap_end_y)):
            for x in range(int(minimap_start_x), int(minimap_end_x)):
                tile_screen_x = (x - minimap_start_x) * tile_scale_x
                tile_screen_y = (y - minimap_start_y) * tile_scale_y

                if 0 <= y < self.engine.MAP_ROWS and 0 <= x < self.engine.MAP_COLS:
                    tile_type = self.engine.map_layout[y][x]
                    if tile_type == 0:
                        color = (50, 150, 50)
                    elif tile_type == 1:
                        color = (139, 69, 19)
                    elif tile_type == 2:
                        color = (173, 216, 230)
                    elif tile_type == 3:
                        color = (200, 50, 50)
                    elif tile_type == 4:
                        color = (100, 100, 100)
                    elif tile_type == 5:
                        color = (173, 216, 230)
                    else:
                        color = (100, 100, 100)
                else:
                    color = (100, 100, 100)

                pygame.draw.rect(
                    minimap_surface,
                    color,
                    (tile_screen_x, tile_screen_y, tile_scale_x, tile_scale_y),
                )

        player_minimap_x = (self.engine.player_pos[0] / self.engine.TILE_SIZE - minimap_start_x) * tile_scale_x
        player_minimap_y = (self.engine.player_pos[1] / self.engine.TILE_SIZE - minimap_start_y) * tile_scale_y
        pygame.draw.circle(
            minimap_surface,
            (0, 0, 255),
            (player_minimap_x, player_minimap_y),
            4
        )

        self.screen.blit(minimap_surface, (10, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.engine.handle_movement(keys)
            self.engine.update_player_position()

            offset_x = self.SCREEN_WIDTH // 2 - self.engine.player_pos[0]
            offset_y = self.SCREEN_HEIGHT // 2 - self.engine.player_pos[1]
            offset_x = min(0, max(offset_x, self.SCREEN_WIDTH - self.engine.MAP_WIDTH))
            offset_y = min(0, max(offset_y, self.SCREEN_HEIGHT - self.engine.MAP_HEIGHT))

            self.screen.fill((255, 255, 255))
            self.draw_map(offset_x, offset_y)
            self.draw_player(offset_x, offset_y)
            self.draw_minimap()
            pygame.display.flip()
            self.clock.tick(self.FPS)


if True:
    pygame.init()
    engine = Engine(map_file="map.txt", tile_size=50, player_size=25, player_speed=5, run_speed_multiplier=2)
    display = Display(engine, screen_width=1000, screen_height=800, fps=60)
    display.run()
