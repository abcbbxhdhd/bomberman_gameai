class Explosion:

    bomber = None

    def __init__(self, x, y, r):
        self.sourceX = x
        self.sourceY = y
        self.range = r
        self.time = 300
        self.sectors = []

    def explode(self, map, bombs, b):

        self.bomber = b.bomber
        self.sectors.extend(b.sectors)
        bombs.remove(b)
        self.bomb_chain(bombs, map)

    def bomb_chain(self, bombs, map):

        for s in self.sectors:
            for bomb in bombs:
                if bomb.pos_x == s[0] and bomb.pos_y == s[1]:
                    map[bomb.pos_x][bomb.pos_y] = 0
                    bomb.bomber.bomb_limit += 1
                    self.explode(map, bombs, bomb)

    def clear_sectors(self, map):

        for x, y in self.sectors:
            map[x][y] = 0

    def update(self, dt):

        self.time -= dt