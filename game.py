import pygame
import sys
import random

from player import Player
from explosion import Explosion
from enemy import Enemy
from enums.algorithm import Algorithm

BACKGROUND_COLOR = (107, 142, 35)

font = None

player = None
enemy_list = []
ene_blocks = []
bombs = []
explosions = []

GRID_BASE = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def game_init(surface, en1_alg, en2_alg, en3_alg, scale):

    global font
    font = pygame.font.SysFont('Bebas', scale)

    global enemy_list
    global ene_blocks
    global player

    enemy_list = []
    ene_blocks = []
    global explosions
    global bombs
    bombs.clear()
    explosions.clear()

    player = Player()

    ene_blocks.append(player)

    if en1_alg is not Algorithm.NONE:
        en1 = Enemy(11, 11, en1_alg)
        enemy_list.append(en1)
        ene_blocks.append(en1)

    if en2_alg is not Algorithm.NONE:
        en2 = Enemy(1, 11, en2_alg)
        enemy_list.append(en2)
        ene_blocks.append(en2)

    if en3_alg is not Algorithm.NONE:
        en3 = Enemy(11, 1, en3_alg)
        enemy_list.append(en3)
        ene_blocks.append(en3)

    grass_img = pygame.transform.scale(pygame.image.load('images/grass.png'), (scale, scale))
    block_img = pygame.transform.scale(pygame.image.load('images/block.png'), (scale, scale))
    box_img = pygame.transform.scale(pygame.image.load('images/box.png'), (scale, scale))
    bomb_image = pygame.transform.scale(pygame.image.load('images/bomb.png'), (scale, scale))
    explosion_image = pygame.transform.scale(pygame.image.load('images/explosion.png'), (scale, scale))

    terrain_images = [grass_img, block_img, box_img, grass_img]

    main(surface, scale, terrain_images, bomb_image, explosion_image)


def draw(s, grid, tile_size, game_ended, terrain_images, bomb_image, explosion_image):
    s.fill(BACKGROUND_COLOR)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            s.blit(terrain_images[grid[i][j]], (i * tile_size, j * tile_size, tile_size, tile_size))

    for x in bombs:
        s.blit(bomb_image, (x.pos_x * tile_size, x.pos_y * tile_size, tile_size, tile_size))

    for y in explosions:
        for x in y.sectors:
            s.blit(explosion_image, (x[0] * tile_size, x[1] * tile_size, tile_size, tile_size))
    if player.life:
        s.blit(player.image,
               (player.pos_x * (tile_size / 4), player.pos_y * (tile_size / 4), tile_size, tile_size))
    for en in enemy_list:
        if en.life:
            s.blit(en.image,
                   (en.pos_x * (tile_size / 4), en.pos_y * (tile_size / 4), tile_size, tile_size))

    if game_ended:
        tf = font.render("Press ESC to go back to menu", False, (153, 153, 255))
        s.blit(tf, (10, 10))

    pygame.display.update()


def generate_map(grid):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 7:
                grid[i][j] = 2

    return


def main(s, tile_size, terrain_images, bomb_image, explosion_image):

    grid = [row[:] for row in GRID_BASE]
    generate_map(grid)
    clock = pygame.time.Clock()

    running = True
    game_ended = False
    while running:
        dt = clock.tick(15)
        for en in enemy_list:
            en.make_move(grid, bombs, explosions, ene_blocks)

        if player.life:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                player.move(0, 1, grid, ene_blocks)
            elif keys[pygame.K_RIGHT]:
                player.move(1, 0, grid, ene_blocks)
            elif keys[pygame.K_UP]:
                player.move(0, -1, grid, ene_blocks)
            elif keys[pygame.K_LEFT]:
                player.move(-1, 0, grid, ene_blocks)

        draw(s, grid, tile_size, game_ended, terrain_images, bomb_image, explosion_image)

        if not game_ended:
            game_ended = check_end_game()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if player.bomb_limit == 0 or not player.life:
                        continue
                    temp_bomb = player.plant_bomb(grid)
                    bombs.append(temp_bomb)
                    grid[temp_bomb.pos_x][temp_bomb.pos_y] = 3
                    player.bomb_limit -= 1
                elif e.key == pygame.K_ESCAPE:
                    running = False

        update_bombs(grid, dt)

    explosions.clear()
    enemy_list.clear()
    ene_blocks.clear()


def update_bombs(grid, dt):
    for b in bombs:
        b.update(dt)
        if b.time < 1:
            b.bomber.bomb_limit += 1
            grid[b.pos_x][b.pos_y] = 0
            exp_temp = Explosion(b.pos_x, b.pos_y, b.range)
            exp_temp.explode(grid, bombs, b)
            exp_temp.clear_sectors(grid)
            explosions.append(exp_temp)
    if player not in enemy_list:
        player.check_death(explosions)
    for en in enemy_list:
        en.check_death(explosions)
    for e in explosions:
        e.update(dt)
        if e.time < 1:
            explosions.remove(e)


def check_end_game():
    if not player.life:
        return True

    for en in enemy_list:
        if en.life:
            return False

    return True
