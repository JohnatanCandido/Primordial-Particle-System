import math
import config
from random import randint

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (247, 5, 218)
BLUE = (0, 0, 255)

MAX_ANGLE_IN_RADIANS = 6.283185307179586


def angle_to_radian(angle):
    return angle * (math.pi / 180)


def radian_to_angle(radian):
    return radian * 180 / math.pi


def normalize_angle(angle):
    if angle < 0:
        return angle + 360
    elif angle > 360:
        return angle - 360
    return angle


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


class Particle:

    def __init__(self, id, x, y, params):
        self.id = id

        self.x = x
        self.y = y

        self.a = params['a']  # alpha
        self.b = params['b']  # beta
        self.r = params['r']  # radius (raio em que considera as outras particulas)
        self.v = params['v']  # velocidade

        self.o = angle_to_radian(randint(0, 360))
        # self.o = angle_to_radian(45)

        self.color = GREEN

        self.nearby = set()

    def __str__(self):
        return f'id: {self.id} - ({self.x}, {self.y})'

    def move(self):
        dx = math.cos(self.o)
        dy = math.sin(self.o)
        self.x += dx * self.v
        self.y += dy * self.v

    def step(self):
        self.tilt()
        self.add_angle(self.a)
        self.move()

    def add_angle(self, angle):
        self.o += angle_to_radian(angle)
        while self.o > MAX_ANGLE_IN_RADIANS:
            self.o -= MAX_ANGLE_IN_RADIANS

    def tilt(self):
        n = 0
        left = 0
        right = 0
        for particle in [p for p in self.nearby if self.in_range(p)]:
            if self.id != particle.id:
                neighbor_type = self.neighbor_type(particle)
                if neighbor_type > -1:
                    n += 1
                    if self.check_side(particle.x, particle.y, neighbor_type) == 'Right':
                        right += 1
                    else:
                        left += 1
        self.add_angle(sign(right - left) * self.b * n)
        self.alter_color(n)

    def neighbor_type(self, particle):
        width = config.MAX_WIDTH - config.MIN_WIDTH
        height = config.MAX_HEIGHT - config.MIN_HEIGHT
        distance = abs(math.sqrt(((self.x - particle.x) ** 2) + ((self.y - particle.y) ** 2)))
        if distance <= self.r:
            return 0
        if self.x - self.r > config.MIN_WIDTH and self.x + self.r < config.MAX_WIDTH \
                and self.y - self.r > config.MIN_HEIGHT and self.y + self.r < config.MAX_HEIGHT:
            return -1
        distance_w = abs(math.sqrt((((self.x + width) - particle.x) ** 2) + ((self.y - particle.y) ** 2)))
        if distance_w:
            return 1
        distance_h = abs(math.sqrt(((self.x - particle.x) ** 2) + (((self.y + height) - particle.y) ** 2)))
        if distance_h:
            return 2
        distance_wh = abs(math.sqrt((((self.x + width) - particle.x) ** 2) + (((self.y + height) - particle.y) ** 2)))
        if distance_wh:
            return 3
        distance_nw = abs(math.sqrt((((self.x - width) - particle.x) ** 2) + ((self.y - particle.y) ** 2)))
        if distance_nw:
            return 4
        distance_nh = abs(math.sqrt(((self.x - particle.x) ** 2) + (((self.y - height) - particle.y) ** 2)))
        if distance_nh:
            return 5
        distance_pwnh = abs(math.sqrt((((self.x + width) - particle.x) ** 2) + (((self.y - height) - particle.y) ** 2)))
        if distance_pwnh:
            return 6
        distance_nwph = abs(math.sqrt((((self.x - width) - particle.x) ** 2) + (((self.y + height) - particle.y) ** 2)))
        if distance_nwph:
            return 7
        distance_nwnh = abs(math.sqrt((((self.x - width) - particle.x) ** 2) + (((self.y - height) - particle.y) ** 2)))
        if distance_nwnh:
            return 8
        return -1

    def in_range(self, particle):
        width = config.MAX_WIDTH - config.MIN_WIDTH
        height = config.MAX_HEIGHT - config.MIN_HEIGHT
        if self.x - self.r <= particle.x <= self.x + self.r and self.y - self.r <= particle.y <= self.y + self.r:
            return True
        if self.x - self.r > config.MIN_WIDTH and self.x + self.r < config.MAX_WIDTH \
                and self.y - self.r > config.MIN_HEIGHT and self.y + self.r < config.MAX_HEIGHT:
            return False
        if self.x + width - self.r <= particle.x <= self.x + width + self.r and self.y - self.r <= particle.y <= self.y + self.r:
            return True
        if self.x - width - self.r <= particle.x <= self.x - width + self.r and self.y - self.r <= particle.y <= self.y + self.r:
            return True
        if self.x - self.r <= particle.x <= self.x + self.r and self.y + height - self.r <= particle.y <= self.y + height + self.r:
            return True
        if self.x - self.r <= particle.x <= self.x + self.r and self.y - height - self.r <= particle.y <= self.y - height + self.r:
            return True
        if self.x + width - self.r <= particle.x <= self.x + width + self.r and self.y + height - self.r <= particle.y <= self.y + height + self.r:
            return True
        if self.x - width - self.r <= particle.x <= self.x - width + self.r and self.y - height - self.r <= particle.y <= self.y - height + self.r:
            return True
        if self.x + width - self.r <= particle.x <= self.x + width + self.r and self.y - height - self.r <= particle.y <= self.y - height + self.r:
            return True
        if self.x - width - self.r <= particle.x <= self.x - width + self.r and self.y + height - self.r <= particle.y <= self.y + height + self.r:
            return True
        return False

    def check_side(self, x, y, neighbor_type):
        if neighbor_type in [1, 3, 6]:
            x += (config.MAX_WIDTH - config.MIN_WIDTH)
        elif neighbor_type in [4, 7, 8]:
            x -= (config.MAX_WIDTH - config.MIN_WIDTH)
        if neighbor_type in [2, 3, 7]:
            y += (config.MAX_HEIGHT - config.MIN_HEIGHT)
        elif neighbor_type in [5, 6, 8]:
            y -= (config.MAX_HEIGHT - config.MIN_HEIGHT)
        angle = radian_to_angle(math.atan2(y - self.y, x - self.x))
        angle = normalize_angle(angle)
        o_angle = radian_to_angle(self.o)
        difference = normalize_angle(o_angle - angle)

        if difference >= 180:
            return 'Right'
        else:
            return 'Left'

    def alter_color(self, n):
        if self.id == 1:
            self.color = (255, 0, 0)
            return
        # self.color = (0, 255, 0)
        if n < 13:
            self.color = GREEN
        elif 13 <= n <= 15:
            self.color = MAGENTA
        elif 15 < n <= 35:
            self.color = BLUE
        elif n > 35:
            self.color = YELLOW


if __name__ == '__main__':
    pass
