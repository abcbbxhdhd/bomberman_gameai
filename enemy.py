import pygame
from bomb import Bomb
import heapq

def get_safety_cost(cell):
    if cell == 2:  # Destroyable
        return float('inf')
    elif cell == 3:  # Unreachable
        return float('inf')
    elif cell == 4:  # Enemy
        return float('inf')
    return 1  # Safe and Enemy

def get_safety_path(game_map, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next = (current[0] + dx, current[1] + dy)
            if 0 <= next[0] < len(game_map) and 0 <= next[1] < len(game_map[0]):
                new_cost = cost_so_far[current] + get_safety_cost(game_map[next[0]][next[1]])
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

    return came_from, cost_so_far

def search_safety(game_map, start):
    goal = None
    min_distance = float('inf')

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 0:
                path, cost = get_safety_path(game_map, start, (x, y))
                total_sum = 0
                for coord in reconstruct_path(path, start, (x, y)):
                    value = cost.get(coord, 0)
                    total_sum += value
                if total_sum != 0 and path and total_sum < min_distance:
                    min_distance = total_sum
                    goal = (x, y)

    if goal is None:
        return None

    final_path, _ = get_safety_path(game_map, start, goal)

    return reconstruct_path(final_path, start, goal)


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_cost(cell):
    if cell == 2:  # Destroyable
        return 10
    elif cell == 1:  # Unsafe
        return 5
    elif cell == 3:  # Unreachable
        return float('inf')
    return 1  # Safe and Enemy


def search_victim(game_map, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next = (current[0] + dx, current[1] + dy)
            if 0 <= next[0] < len(game_map) and 0 <= next[1] < len(game_map[0]):
                new_cost = cost_so_far[current] + get_cost(game_map[next[0]][next[1]])
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def get_enemies_coordinates(enemies):
    coordinates = []

    for enemy in enemies:
        coordinates.append((int(enemy.pos_x / Enemy.TILE_SIZE), int(enemy.pos_y / Enemy.TILE_SIZE)))

    return coordinates


def get_direction(current_coords, next_coords):
    dx = next_coords[0] - current_coords[0]
    dy = next_coords[1] - current_coords[1]

    if dy == -1:
        return 2  # Up
    elif dx == 1:
        return 1  # Right
    elif dy == 1:
        return 0  # Down
    elif dx == -1:
        return 3  # Left

class Enemy:
    image = pygame.transform.scale(pygame.image.load('images/enemy.png'), (36, 36))

    TILE_SIZE = 4

    def __init__(self, x, y, alg):
        self.life = True
        self.path = []
        self.movement_path = []
        self.pos_x = x * Enemy.TILE_SIZE
        self.pos_y = y * Enemy.TILE_SIZE
        self.direction = 0
        self.animation = []
        self.range = 2
        self.bomb_limit = 1
        self.plant = False
        self.algorithm = alg

    def move(self, map, bombs, explosions, enemy):
        if self.direction == 0:
            self.pos_y += 1
        elif self.direction == 1:
            self.pos_x += 1
        elif self.direction == 2:
            self.pos_y -= 1
        elif self.direction == 3:
            self.pos_x -= 1

        if self.pos_x % Enemy.TILE_SIZE == 0 and self.pos_y % Enemy.TILE_SIZE == 0:
            self.movement_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                grid = self.create_grid(map, bombs, explosions, enemy)
                next = self.path[1]
                if grid[next[0]][next[1]] > 1:
                    self.movement_path.clear()
                    self.path.clear()

    def make_move(self, map, bombs, explosions, enemy):
        if not self.life:
            return
        if len(self.movement_path) == 0:
            if self.plant:
                bombs.append(self.plant_bomb(map))
                self.plant = False
                map[int(self.pos_x / Enemy.TILE_SIZE)][int(self.pos_y / Enemy.TILE_SIZE)] = 3

            self.dfs(self.create_grid(map, bombs, explosions, enemy), enemy)
        else:
            self.direction = self.movement_path[0]
            self.move(map, bombs, explosions, enemy)

    def plant_bomb(self, map):
        b = Bomb(self.range, round(self.pos_x / Enemy.TILE_SIZE), round(self.pos_y / Enemy.TILE_SIZE), map, self)
        self.bomb_limit -= 1
        return b

    def check_death(self, exp):
        for e in exp:
            for s in e.sectors:
                if int(self.pos_x / Enemy.TILE_SIZE) == s[0] and int(self.pos_y / Enemy.TILE_SIZE) == s[1]:
                    self.life = False
                    return

    def dfs(self, grid, enemies):
        new_path = [[int(self.pos_x / Enemy.TILE_SIZE), int(self.pos_y / Enemy.TILE_SIZE)]]
        depth = 0
        if self.bomb_limit == 0:
            self.dfs_rec(grid, 0, new_path, depth, enemies)
        else:
            self.dfs_rec(grid, 2, new_path, depth, enemies)

        self.path = new_path

    def find_safety(self, grid, coordinates):
        if grid[coordinates[0] + 1][coordinates[1]] == 0:
            return [coordinates[0] + 1, coordinates[1]]
        if grid[coordinates[0] - 1][coordinates[1]] == 0:
            return [coordinates[0] - 1, coordinates[1]]
        if grid[coordinates[0]][coordinates[1] + 1] == 0:
            return [coordinates[0], coordinates[1] + 1]
        if grid[coordinates[0]][coordinates[1] - 1] == 0:
            return [coordinates[0], coordinates[1] - 1]

    def dfs_rec(self, grid, end, path, depth, enemies):
        last = path[-1]
        # stop to prevent infinite useless cycles
        if depth > 200:
            return
        # don't move if you are safe, and you've already planted the bomb
        if grid[last[0]][last[1]] == 0 and end == 0:
            return

        tile_value = grid[last[0]][last[1]]

        came_from, _ = search_victim(grid, (last[0], last[1]), get_enemies_coordinates(enemies)[0])
        new_path = reconstruct_path(came_from, (last[0], last[1]), get_enemies_coordinates(enemies)[0])

        if tile_value != 0:
            path_to_safe = search_safety(grid, (last[0], last[1]))
            if path_to_safe is None:
                return
            path.append([path_to_safe[1][0], path_to_safe[1][1]])
            self.movement_path.append(get_direction(last, path_to_safe[1]))
        elif grid[new_path[1][0]][new_path[1][1]] == 0:
            if len(new_path) < 2:
                return
            path.append(new_path[1])
            self.movement_path.append(get_direction(last, new_path[1]))
        # if you have a bomb
        elif end == 2:
            # and if you've reached destroyable block
            if grid[last[0] + 1][last[1]] in [2, 4] \
                    or grid[last[0] - 1][last[1]] in [2, 4] \
                    or grid[last[0]][last[1] + 1] in [2, 4] \
                    or grid[last[0]][last[1] - 1] in [2, 4]:
                # plant the bomb
                self.plant = True
                return
        else:
            if len(self.movement_path) > 0:
                path.pop(0)
                self.movement_path.pop(0)
        depth += 1
        self.dfs_rec(grid, end, path, depth, enemies)

    def create_grid(self, map, bombs, explosions, enemies):
        grid = [[0] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destroyable
        # 3 - unreachable
        # 4 - ENEMY
        # 5 - ALLIES

        for b in bombs:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]] = 1
            grid[b.pos_x][b.pos_y] = 3

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]] = 3

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    grid[i][j] = 3
                elif map[i][j] == 2:
                    grid[i][j] = 2

        for x in enemies:
            if x == self:
                continue
            elif not x.life:
                continue
            elif isinstance(x, Enemy):
                grid[int(x.pos_x / Enemy.TILE_SIZE)][int(x.pos_y / Enemy.TILE_SIZE)] = 5
            else:
                grid[int(x.pos_x / Enemy.TILE_SIZE)][int(x.pos_y / Enemy.TILE_SIZE)] = 4

        return grid
