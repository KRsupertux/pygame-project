import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Realistic Map with Impassable Obstacles")

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 150, 50)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (200, 50, 50)  # Obstacle color
GRAY = (100, 100, 100)  # Road color
LIGHT_BLUE = (173, 216, 230)  # River color
BLACK=(0,0,0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Tile size and map dimensions
TILE_SIZE = 50
MAP_ROWS = 60
MAP_COLS = 150
MAP_WIDTH = MAP_COLS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE

# Player setup
player_size = TILE_SIZE // 2
player_color = BLUE
player_pos = [MAP_WIDTH // 2, MAP_HEIGHT // 2]
player_velocity = [0, 0]

# Movement constants
player_speed = 5
run_speed_multiplier = 2

# Textures for terrain
grass_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
grass_texture.fill(GREEN)

dirt_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
dirt_texture.fill(BROWN)

water_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
water_texture.fill(LIGHT_BLUE)

road_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
road_texture.fill(GRAY)

rock_texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
rock_texture.fill(RED)

# Map design
map_layout = [[random.choice([0, 1]) for _ in range(MAP_COLS)] for _ in range(MAP_ROWS)]

# Add roads
for _ in range(10):  # Vertical roads
    road_x = random.randint(0, MAP_COLS - 1)
    for y in range(MAP_ROWS):
        map_layout[y][road_x] = 4

for _ in range(10):  # Horizontal roads
    road_y = random.randint(0, MAP_ROWS - 1)
    for x in range(MAP_COLS):
        map_layout[road_y][x] = 4

# Add rivers
for _ in range(5):  # Add 5 rivers
    river_start_x = random.randint(0, MAP_COLS - 1)
    river_y = random.randint(0, MAP_ROWS - 1)
    for _ in range(random.randint(20, 50)):  # River length
        map_layout[river_y][river_start_x] = 5
        river_start_x += random.choice([-1, 0, 1])
        river_y += random.choice([-1, 0, 1])
        river_start_x = max(0, min(river_start_x, MAP_COLS - 1))
        river_y = max(0, min(river_y, MAP_ROWS - 1))

# Add impassable rocks
for _ in range(500):
    x = random.randint(0, MAP_COLS - 1)
    y = random.randint(0, MAP_ROWS - 1)
    if map_layout[y][x] in [0, 1]:  # Place on grass or dirt only
        map_layout[y][x] = 3

# Function to draw the map
def draw_map(offset_x, offset_y):
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            tile_x = col * TILE_SIZE + offset_x
            tile_y = row * TILE_SIZE + offset_y

            if tile_x + TILE_SIZE < 0 or tile_y + TILE_SIZE < 0 or tile_x > SCREEN_WIDTH or tile_y > SCREEN_HEIGHT:
                continue

            if map_layout[row][col] == 0:
                screen.blit(grass_texture, (tile_x, tile_y))
            elif map_layout[row][col] == 1:
                screen.blit(dirt_texture, (tile_x, tile_y))
            elif map_layout[row][col] == 2:
                screen.blit(water_texture, (tile_x, tile_y))
            elif map_layout[row][col] == 3:
                screen.blit(rock_texture, (tile_x, tile_y))
            elif map_layout[row][col] == 4:
                screen.blit(road_texture, (tile_x, tile_y))
            elif map_layout[row][col] == 5:
                screen.blit(water_texture, (tile_x, tile_y))

# Handle player movement
def handle_movement(keys):
    global player_velocity

    # Reset velocity
    player_velocity = [0, 0]

    # Calculate player's current tile
    player_tile_x = player_pos[0] // TILE_SIZE
    player_tile_y = player_pos[1] // TILE_SIZE

    # Movement checks
    if keys[pygame.K_UP]:
        if not is_obstacle(player_tile_x, player_tile_y - 1):
            player_velocity[1] -= player_speed
    if keys[pygame.K_DOWN]:
        if not is_obstacle(player_tile_x, player_tile_y + 1):
            player_velocity[1] += player_speed
    if keys[pygame.K_LEFT]:
        if not is_obstacle(player_tile_x - 1, player_tile_y):
            player_velocity[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        if not is_obstacle(player_tile_x + 1, player_tile_y):
            player_velocity[0] += player_speed

    # Running modifier
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        player_velocity[0] *= run_speed_multiplier
        player_velocity[1] *= run_speed_multiplier

# Check if a tile is an obstacle
def is_obstacle(tile_x, tile_y):
    if 0 <= tile_x < MAP_COLS and 0 <= tile_y < MAP_ROWS:
        return map_layout[tile_y][tile_x] == 3  # Impassable if tile is rock
    return True  # Treat out-of-bounds as impassable

# Update player position
def update_player_position():
    global player_pos

    # Update position with velocity
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Clamp position within map boundaries
    player_pos[0] = max(0, min(player_pos[0], MAP_WIDTH - player_size))
    player_pos[1] = max(0, min(player_pos[1], MAP_HEIGHT - player_size))

def draw_minimap():
    # Minimap dimensions in pixels
    minimap_width = 200
    minimap_height = 150
    minimap_tile_size = 25  # Number of tiles in the minimap

    # Define the region of the map to display on the minimap
    player_tile_x = player_pos[0] / TILE_SIZE
    player_tile_y = player_pos[1] / TILE_SIZE

    # Minimap center is the player's current tile position
    minimap_center_x = player_tile_x
    minimap_center_y = player_tile_y

    # Calculate the minimap's visible area
    minimap_start_x = max(0, minimap_center_x - minimap_tile_size / 2)
    minimap_start_y = max(0, minimap_center_y - minimap_tile_size / 2)

    minimap_end_x = minimap_start_x + minimap_tile_size
    minimap_end_y = minimap_start_y + minimap_tile_size

    # Create a surface for the minimap
    minimap_surface = pygame.Surface((minimap_width, minimap_height))
    minimap_surface.fill(GRAY)  # Default to grey for undefined areas

    # Calculate scale for minimap tiles
    tile_scale_x = minimap_width / minimap_tile_size
    tile_scale_y = minimap_height / minimap_tile_size

    # Draw the minimap content
    for y in range(int(minimap_start_y), int(minimap_end_y)):
        for x in range(int(minimap_start_x), int(minimap_end_x)):
            # Calculate tile position on minimap
            tile_screen_x = (x - minimap_start_x) * tile_scale_x
            tile_screen_y = (y - minimap_start_y) * tile_scale_y

            # Check if the tile is within the map boundaries
            if 0 <= y < MAP_ROWS and 0 <= x < MAP_COLS:
                # Determine the tile color based on the map layout
                if map_layout[y][x] == 0:
                    color = GREEN  # Grass
                elif map_layout[y][x] == 1:
                    color = BROWN  # Dirt
                elif map_layout[y][x] == 2:
                    color = LIGHT_BLUE  # Water
                elif map_layout[y][x] == 3:
                    color = RED  # Rock
                elif map_layout[y][x] == 4:
                    color = GRAY  # Road
                elif map_layout[y][x] == 5:
                    color = LIGHT_BLUE  # River
                else:
                    color = GRAY  # Undefined tiles
            else:
                color = GRAY  # Outside the map boundaries

            # Draw the tile
            pygame.draw.rect(
                minimap_surface,
                color,
                (tile_screen_x, tile_screen_y, tile_scale_x, tile_scale_y),
            )

    # Draw the player on the minimap
    player_minimap_x = (player_pos[0] / TILE_SIZE - minimap_start_x) * tile_scale_x
    player_minimap_y = (player_pos[1] / TILE_SIZE - minimap_start_y) * tile_scale_y
    pygame.draw.circle(
        minimap_surface, 
        BLUE, 
        (int(player_minimap_x), int(player_minimap_y)), 
        5
    )

    # Draw minimap border
    pygame.draw.rect(screen, BLACK, (10, 10, minimap_width + 2, minimap_height + 2), 3)

    # Display the minimap on the screen
    screen.blit(minimap_surface, (10, 10))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle input
    keys = pygame.key.get_pressed()
    handle_movement(keys)

    # Update player position
    update_player_position()

    # Calculate map offset
    offset_x = SCREEN_WIDTH // 2 - player_pos[0]
    offset_y = SCREEN_HEIGHT // 2 - player_pos[1]
    offset_x = min(0, max(offset_x, SCREEN_WIDTH - MAP_WIDTH))
    offset_y = min(0, max(offset_y, SCREEN_HEIGHT - MAP_HEIGHT))

    # Draw the map and player
    screen.fill(WHITE)
    draw_map(offset_x, offset_y)
    pygame.draw.rect(
        screen,
        player_color,
        (SCREEN_WIDTH // 2 - player_size // 2, SCREEN_HEIGHT // 2 - player_size // 2, player_size, player_size),
    )
    draw_minimap()
    # Update display
    pygame.display.flip()
    clock.tick(FPS)
