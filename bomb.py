class Bomb:
    def __init__(self, r, x, y, map, bomber):
        self.range = r
        self.pos_x = x
        self.pos_y = y
        self.time = 3000
        self.bomber = bomber
        self.sectors = []
        self.get_range(map)

    def update(self, dt):

        self.time = self.time - dt

    def check_sector(self, map, delta_x, delta_y):
        for x in range(1, self.range):
            new_x, new_y = self.pos_x + delta_x * x, self.pos_y + delta_y * x
            if map[new_x][new_y] == 1:
                break
            elif map[new_x][new_y] in [0, 2]:
                self.sectors.append([new_x, new_y])
                if map[new_x][new_y] == 2:
                    break

    def get_range(self, map):
        self.sectors.append([self.pos_x, self.pos_y])
        self.check_sector(map, 1, 0)
        self.check_sector(map, -1, 0)
        self.check_sector(map, 0, 1)
        self.check_sector(map, 0, -1)
