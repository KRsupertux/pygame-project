import pygame
import math
import sys
import random

class humanobj:
    def __init__(self,size,color,pos,vel,speed,rsm):
        self.obj_size=size
        self.obj_color=color
        self.obj_pos=pos
        self.obj_vel=vel
        self.obj_speed=speed
        self.obj_rsm=rsm #run_speed_multiplier
    

def run_game_loop():
    pygame.init()
    SCREEN_WIDTH,SCREEN_HEIGHT=1400,800
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    #Colors
    WHITE=(255,255,255)
    GREEN=(50,150,50)
    BROWN=(139,69,19)
    BLUE=(0,0,255)
    RED=(200,50,50)
    GRAY=(100,100,100)
    LIGHT_BLUE=(173,216,230)
    BLACK=(0,0,0)

    clock=pygame.time.Clock()
    FPS=60

    TILE_SIZE=50
    MAP_ROWS=10
    MAP_COLS=10
    MAP_WIDTH=MAP_COLS*TILE_SIZE
    MAP_HEIGHT=MAP_ROWS*TILE_SIZE

    player=humanobj(TILE_SIZE//2,BLUE,[MAP_WIDTH//2,MAP_HEIGHT//2],[0,0],5,1.5)

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
    #open map
    map_layout=[[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2],[1,2,3,4,1,2,3,4,1,2]]
    #with open("./maps/map1.txt",'r') as file:
     #   for line in file:
      #      map_layout.append(list(map(int,line.split())))
       #     if len(line) != MAP_COLS:
        #        raise ValueError(f"Map row length {len(line)}")
      #  if len(map_layout)!=MAP_ROWS:
       #     raise ValueError(f"Map num_row {len(map_layout)}")

    def draw_map(offset_x,offset_y): 
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                tile_x=col*TILE_SIZE+offset_x
                tile_y=row*TILE_SIZE+offset_y

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

    def handle_movement(keys):
        player.obj_vel=[0,0]
        player_tile_x=player.obj_pos[0]//TILE_SIZE
        player_tile_y=player.obj_pos[1]//TILE_SIZE
        check_const=0.2

        if keys[pygame.K_UP]:
            if not is_obstacle(player_tile_x,player_tile_y-check_const):
                player.obj_vel[1]-=player.obj_speed
        if keys[pygame.K_DOWN]:
            if not is_obstacle(player_tile_x,player_tile_y+check_const):
                player.obj_vel[1]+=player.obj_speed
        if keys[pygame.K_LEFT]:
            if not is_obstacle(player_tile_x-check_const,player_tile_y):
                player.obj_vel[0]-=player.obj_speed
        if keys[pygame.K_RIGHT]:
            if not is_obstacle(player_tile_x+check_const,player_tile_y):
                player.obj_vel[0]+=player.obj_speed

        if keys[pygame.K_LSHIFT]:
            player.obj_vel[0]*=player.obj_rsm
            player.obj_vel[1]*=player.obj_rsm

    def is_obstacle(tile_x,tile_y):
        if 0<=tile_x<MAP_COLS and 0<=tile_y<MAP_ROWS:
            return map_layout[math.floor(tile_y)][math.floor(tile_x)]==3
        return True

    def update_player_position():
        player.obj_pos[0]+=player.obj_vel[0]
        player.obj_pos[1]+=player.obj_vel[1]

        player.obj_pos[0]=max(0,min(player.obj_pos[0],MAP_WIDTH-player.obj_size))
        player.obj_pos[1]=max(0,min(player.obj_pos[1],MAP_HEIGHT-player.obj_size))

    def draw_minimap():
        minimap_width=200
        minimap_height=150
        minimap_tile_size=25

        player_tile_x=player.obj_pos[0]/TILE_SIZE
        player_tile_y=player.obj_pos[1]/TILE_SIZE

        minimap_center_x=player_tile_x
        minimap_center_y=player_tile_y

        minimap_start_x=max(0,minimap_center_x-minimap_tile_size/2)
        minimap_start_y=max(0,minimap_center_y-minimap_tile_size/2)

        minimap_end_x=minimap_start_x+minimap_tile_size
        minimap_end_y=minimap_start_y+minimap_tile_size

        minimap_surface=pygame.Surface((minimap_width,minimap_height))
        minimap_surface.fill(GRAY)

        tile_scale_x=minimap_width/minimap_tile_size
        tile_scale_y=minimap_height/minimap_tile_size

        for y in range(int(minimap_start_y),int(minimap_end_y)):
            for x in range(int(minimap_start_x),int(minimap_end_x)):
                tile_screen_x=(x-minimap_start_x)*tile_scale_x
                tile_screen_y=(y-minimap_start_y)*tile_scale_y
#define: map colors
# 0 grass 1 dirt 2 water 3 rock 4 road 5 river 
                if 0<=y<MAP_ROWS and 0<=x<MAP_COLS:
                    if map_layout[y][x]==0:
                        color=GREEN
                    elif map_layout[y][x]==1:
                        color=BROWN
                    elif map_layout[y][x]==2:
                        color=LIGHT_BLUE
                    elif map_layout[y][x]==3:
                        color=RED
                    elif map_layout[y][x]==4:
                        color=GRAY
                    elif map_layout[y][x]==5:
                        color=LIGHT_BLUE
                    else:#undefined
                        color=GRAY
                else:#out_of_bounds
                    color=GRAY
                pygame.draw.rect(
                    minimap_surface,
                    color,
                    (tile_screen_x,tile_screen_y,tile_scale_x,tile_scale_y),
                )

        player_minimap_x=(player.obj_pos[0]/TILE_SIZE-minimap_start_x)*tile_scale_x
        player_minimap_y=(player.obj_pos[1]/TILE_SIZE-minimap_start_y)*tile_scale_y
        pygame.draw.circle(
            minimap_surface,
            BLUE,
            (int(player_minimap_x),int(player_minimap_y)),
            5
        )

        pygame.draw.rect(screen,BLACK,(10,10,minimap_width+2,minimap_height+2),3)
        screen.blit(minimap_surface,(10,10))

    def game_loop():
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys=pygame.key.get_pressed()
            handle_movement(keys)

            update_player_position()
            offset_x=SCREEN_WIDTH//2-player.obj_pos[0]
            offset_y=SCREEN_HEIGHT//2-player.obj_pos[1]
            offset_x=min(0,max(offset_x,SCREEN_WIDTH-MAP_WIDTH))
            offset_y=min(0,max(offset_y,SCREEN_HEIGHT-MAP_HEIGHT))

            screen.fill(WHITE)
            draw_map(offset_x,offset_y)
            pygame.draw.rect(
                screen,
                player.obj_color,
                (int(SCREEN_WIDTH//2-player.obj_size//2),int(SCREEN_HEIGHT//2-player.obj_size//2),int(player.obj_size),int(player.obj_size)),
            )
            draw_minimap()
            pygame.display.flip()
            clock.tick(FPS)
    game_loop()
run_game_loop()
