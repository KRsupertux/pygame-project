"""
저장 기능을 추가하자
"""

import pygame as pg
import sys

# pickle, os 모듈을 불러온다
import pickle
import os

from pygame.examples.cursors import image

pg.init()

SCREEN_W = 800
SCREEN_H = 600

WHITE = (255, 255, 255)
SKYBLUE = (135, 206, 235)
RED = (255, 0, 0)
# 색상 추가
YELLOW = (255, 255, 0)

FPS = 60

TILE_SIZE = 40

screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("pakour")
clock = pg.time.Clock()


maps = [
    [
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "...E.P...F....G.....",
        "...##############...",
        "....................",
        "....................",
        "....................",
        "....................",
    ],
    [
        "....................",
        "....................",
        "...G................",
        "..#####.............",
        "..........#.E.......",
        "...........##.......",
        "....................",
        "...............##...",
        "........F...........",
        ".......#####........",
        "...............##...",
        "............E.......",
        "...........########.",
        ".P...F..............",
        "########............",
    ],
]


class Character(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False

    def update(self, grounds):
        self.rect.x += self.speed_x / FPS
        self.collide_x(grounds)
        self.rect.y += self.speed_y / FPS
        self.collide_y(grounds)

    def collide_x(self, grounds):
        for ground in pg.sprite.spritecollide(self, grounds, False):
            if self.speed_x > 0:
                self.rect.right = ground.rect.left
            elif self.speed_x < 0:
                self.rect.left = ground.rect.right

    def collide_y(self, grounds):
        for ground in pg.sprite.spritecollide(self, grounds, False):
            if self.speed_y > 0:
                self.rect.bottom = ground.rect.top
                self.speed_y = 0
                self.on_ground = True
            elif self.speed_y < 0:
                self.rect.top = ground.rect.bottom
                self.speed_y = 0

images = {
    "smallleftstop": pg.image.load("data/smallleftstop.png"),
    "smallleftwalking1": pg.image.load("data/smallleftwalking1.png"),
    "smallleftwalking2": pg.image.load("data/smallleftwalking2.png"),
    "smallrightstop": pg.image.load("data/smallrightstop.png"),
    "smallrightwalking1": pg.image.load("data/smallrightwalking1.png"),
    "smallrightwalking2": pg.image.load("data/smallrightwalking2.png"),
}
class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE)
        self.image = pg.image.load("data/downstop.png")
        self.is_moving = False
        self.frame_count = 0
        self.player_state_idx = "left"
        self.on_ground = True
        self.image_size = (150, 150)

    def update(self, grounds):
        self.move()
        self.update_image()
        super().update(grounds)

    def move(self):
        self.speed_y += 30

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.speed_x = -300
            self.player_state_idx = "left"
            self.is_moving = True
        elif keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.speed_x = 300
            self.player_state_idx = "right"
            self.is_moving = True
        else:
            self.speed_x = 0
            self.is_moving = False

        if keys[pg.K_UP]:
            if self.on_ground:
                self.speed_y = -600
                self.on_ground = False

    def shoot(self, target_x, target_y, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update_image(self):
        global images

        if self.is_moving:
            self.frame_count += 1
            if self.frame_count // 10 % 2 == 0:
                image_key = f"small{self.player_state_idx}walking1"
            else:
                image_key = f"small{self.player_state_idx}walking2"
        else:
            image_key = f"small{self.player_state_idx}stop"

        original_image = images[image_key]
        self.image = pg.transform.scale(original_image, self.image_size)



class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.speed_x = 0
        ori_image = pg.image.load("data/cone.png")
        self.image = pg.transform.scale(ori_image, (150,150))

    def is_on_edge(self, grounds):
        if self.speed_x > 0:
            sensor = pg.Rect(
                self.rect.right + self.speed_x / FPS, self.rect.bottom, 1, 1
            )
        else:
            sensor = pg.Rect(
                self.rect.left + self.speed_x / FPS, self.rect.bottom, 1, 1
            )
        for ground in grounds:
            if sensor.colliderect(ground.rect):
                return False
        return True


class Goal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("data/portal.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pg.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        dx = target_x - x
        dy = target_y - y
        dist = (dx * dx + dy * dy) ** 0.5
        self.speed_x = 600 * dx / dist
        self.speed_y = 600 * dy / dist

    def update(self, grounds):
        self.rect.x += self.speed_x / FPS
        self.rect.y += self.speed_y / FPS

        if (
            self.rect.right < 0
            or self.rect.left > SCREEN_W
            or self.rect.bottom < 0
            or self.rect.top > SCREEN_H
        ):
            self.kill()
        for ground in grounds:
            if pg.sprite.collide_rect(self, ground):
                self.kill()


class Flag(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("data/flag.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def load_level(level):
    all_sprites = pg.sprite.Group()
    player = None
    goal = None
    grounds = pg.sprite.Group()
    enemies = pg.sprite.Group()
    bullets = pg.sprite.Group()
    # 게임을 저장하는 위치를 표시하는 깃발을 추가한다
    flags = pg.sprite.Group()

    map = maps[level]
    for row_idx, row in enumerate(map):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile == "#":
                ground = pg.sprite.Sprite()
                ground.image = pg.image.load("data/dirt.png")
                ground.rect = ground.image.get_rect()
                ground.rect.topleft = (x, y)
                grounds.add(ground)
                all_sprites.add(ground)
            elif tile == "P":
                player = Player(x, y)
                all_sprites.add(player)
            elif tile == "G":
                goal = Goal(x, y)
                all_sprites.add(goal)
            elif tile == "E":
                enemy = Enemy(x, y)
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif tile == "F":
                flag = Flag(x, y)
                flags.add(flag)
                all_sprites.add(flag)

    if player is None:
        raise Exception("No player in the map")
    if goal is None:
        raise Exception("No goal in the map")

    return all_sprites, player, goal, grounds, enemies, bullets, flags


def game_loop(level=0, pos=None):
    all_sprites, player, goal, grounds, enemies, bullets, flags = load_level(level)

    # 플레이어의 위치를 이어받아서 게임을 시작한다
    if pos:
        player.rect.topleft = pos
    time_list = []
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                elif event.key == pg.K_SPACE:
                    pass
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(event.pos[0], event.pos[1], all_sprites, bullets)

        player.update(grounds)
        goal.update()
        grounds.update()
        enemies.update(grounds)
        bullets.update(grounds)

        if len(time_list) == 10:
            time_list.pop(0)
        time_list.append((player, enemies))

        if pg.sprite.collide_rect(player, goal):
            level += 1
            if level >= len(maps):
                print("Game Clear!")
                return
            all_sprites, player, goal, grounds, enemies, bullets, flags = load_level(
                level
            )

        if pg.sprite.spritecollide(player, enemies, False):
            print("Game Over!")
            return

        if player.rect.top > SCREEN_H:
            print("Game Over!")
            return

        # 깃발을 획득하면 게임을 저장한다
        for flag in pg.sprite.spritecollide(player, flags, False):
            print("Game saved!")
            # 깃발을 제거한다
            flag.kill()
            # 레벨과 플레이어의 위치를 저장한다
            save_game(level, player.rect.topleft)

        for enemy in pg.sprite.groupcollide(enemies, bullets, True, True):
            print(f"Enemy killed at {enemy.rect.center}")

        screen.fill(SKYBLUE)
        all_sprites.draw(screen)

        pg.display.update()
        clock.tick(FPS)


def main_menu():
    menu_options = ["Start New Game", "Load Game", "Quit"]
    selected_option = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pg.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pg.K_RETURN:
                    if selected_option == 0:
                        game_loop()
                    elif selected_option == 1:
                        # 저장된 게임을 불러온다
                        level, pos = load_game()
                        game_loop(level, pos)
                    elif selected_option == 2:
                        sys.exit()
        screen.fill(SKYBLUE)
        title_font = pg.font.Font(None, 80)
        title_text = title_font.render("Square Adventure", True, WHITE)
        screen.blit(title_text, (SCREEN_W // 2 - title_text.get_width() // 2, 100))
        menu_font = pg.font.Font(None, 40)
        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected_option else WHITE
            text = menu_font.render(option, True, color)
            screen.blit(
                text,
                (SCREEN_W // 2 - text.get_width() // 2, SCREEN_H // 2 + i * 60),
            )
        pg.display.update()
        clock.tick(FPS)


# 게임을 파일에 저장한다
def save_game(level, pos):
    with open("savefile", "wb") as f:
        pickle.dump((level, pos), f)


# 게임 저장 파일을 불러온다
def load_game():
    if os.path.exists("savefile"):
        with open("savefile", "rb") as f:
            return pickle.load(f)
    return 0, None  # Default to first level if no save is found


if __name__ == "__main__":
    main_menu()
