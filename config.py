DRAW_R_LINE = False
TICK = 60

PARTICLE_RADIUS = 5
PARTICLE_NUMBER = 1000

PARTICLE_PARAMETERS = {'a': 180,
                       'b': 17,
                       'r': 50,
                       'v': 6.7}

WIDTH = 1500
HEIGHT = 900

MIN_WIDTH = 0
MIN_HEIGHT = 0

MAX_WIDTH = 1500
MAX_HEIGHT = 900

CELL_DIMENSIONS = [(MAX_WIDTH - MIN_WIDTH) / 50, (MAX_HEIGHT - MIN_HEIGHT) / 50]
# CELL_DIMENSIONS = [MAX_WIDTH, MAX_HEIGHT]


def change_size(min_width, max_width, min_height, max_height):
    global MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT
    MIN_WIDTH = min_width
    MAX_WIDTH = max_width
    MIN_HEIGHT = min_height
    MAX_HEIGHT = max_height


def flip_draw_r_line():
    global DRAW_R_LINE
    DRAW_R_LINE = not DRAW_R_LINE


if __name__ == '__main__':
    pass
