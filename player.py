import pygame
import math

from bomb import Bomb


class Player:
    TILE_SIZE = 4
    image = pygame.transform.scale(pygame.image.load('images/player.png'), (36, 36))

    def __init__(self, x=4, y=4, bomb_range=3, bomb_limit=1):
        self.pos_x = x
        self.pos_y = y
        self.range = bomb_range
        self.bomb_limit = bomb_limit
        self.life = True

    def move(self, dx, dy, grid, enemies):
        tempx = int(self.pos_x / Player.TILE_SIZE)
        tempy = int(self.pos_y / Player.TILE_SIZE)

        map = []

        for i in range(len(grid)):
            map.append([])
            for j in range(len(grid[i])):
                map[i].append(grid[i][j])

        for x in enemies:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                map[int(x.pos_x / Player.TILE_SIZE)][int(x.pos_y / Player.TILE_SIZE)] = 2

        if self.pos_x % Player.TILE_SIZE != 0 and dx == 0:
            if self.pos_x % Player.TILE_SIZE == 1:
                self.pos_x -= 1
            elif self.pos_x % Player.TILE_SIZE == 3:
                self.pos_x += 1
            return
        if self.pos_y % Player.TILE_SIZE != 0 and dy == 0:
            if self.pos_y % Player.TILE_SIZE == 1:
                self.pos_y -= 1
            elif self.pos_y % Player.TILE_SIZE == 3:
                self.pos_y += 1
            return

        # right
        if dx == 1:
            if map[tempx+1][tempy] == 0:
                self.pos_x += 1
        # left
        elif dx == -1:
            tempx = math.ceil(self.pos_x / Player.TILE_SIZE)
            if map[tempx-1][tempy] == 0:
                self.pos_x -= 1

        # bottom
        if dy == 1:
            if map[tempx][tempy+1] == 0:
                self.pos_y += 1
        # top
        elif dy == -1:
            tempy = math.ceil(self.pos_y / Player.TILE_SIZE)
            if map[tempx][tempy-1] == 0:
                self.pos_y -= 1

    def plant_bomb(self, map):
        return Bomb(self.range, round(self.pos_x / Player.TILE_SIZE), round(self.pos_y / Player.TILE_SIZE), map, self)

    def check_death(self, explosions):
        for e in explosions:
            for s in e.sectors:
                if int(self.pos_x / Player.TILE_SIZE) == s[0] and int(self.pos_y / Player.TILE_SIZE) == s[1]:
                    self.life = False
