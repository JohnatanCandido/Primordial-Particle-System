import pygame
import config
from particle import Particle
from random import randint
from spatial_hash_grid import SpatialHashGrid

pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

game_display = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
clock = pygame.time.Clock()


particles = []
grid = SpatialHashGrid([[config.MIN_WIDTH, config.MAX_WIDTH],
                        [config.MIN_HEIGHT, config.MAX_HEIGHT]], config.CELL_DIMENSIONS)
mouse_start_x, mouse_start_y = 0, 0
change_size = False


def main_loop():
    init_particles()
    running = True

    while running:
        check_input()
        game_display.fill(BLACK)
        draw_spawn_area()
        draw_particles()
        draw_limits()
        pygame.display.update()
        clock.tick(config.TICK)


def check_input():
    global mouse_start_x, mouse_start_y, change_size
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3)[0]:
                # particles[1].x = pygame.mouse.get_pos()[0]
                # particles[1].y = pygame.mouse.get_pos()[1]
                add_particle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif pygame.mouse.get_pressed(3)[1] or pygame.mouse.get_pressed(3)[2]:
                particles.clear()
                mouse_start_x = pygame.mouse.get_pos()[0]
                mouse_start_y = pygame.mouse.get_pos()[1]
            change_size = pygame.mouse.get_pressed(3)[1]
        if event.type == pygame.MOUSEBUTTONUP and mouse_start_x > 0:
            mouse_end_x = pygame.mouse.get_pos()[0]
            mouse_end_y = pygame.mouse.get_pos()[1]

            if change_size:
                config.change_size(min(mouse_start_x, mouse_end_x),
                                   max(mouse_start_x, mouse_end_x),
                                   min(mouse_start_y, mouse_end_y),
                                   max(mouse_start_y, mouse_end_y))
                init_particles()
            else:
                create_particles(config.PARTICLE_NUMBER,
                                 min(mouse_start_x, mouse_end_x),
                                 max(mouse_start_x, mouse_end_x),
                                 min(mouse_start_y, mouse_end_y),
                                 max(mouse_start_y, mouse_end_y))

            mouse_start_x, mouse_start_y = 0, 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                init_particles()
            elif event.key == pygame.K_r:
                config.flip_draw_r_line()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mx = pygame.mouse.get_pos()[0]
        #     my = pygame.mouse.get_pos()[1]
        #
        #     p = particles[0]
        #
        #     print(p.check_side(mx, my))


def draw_spawn_area():
    if mouse_start_x != 0:
        w = pygame.mouse.get_pos()[0] - mouse_start_x
        h = pygame.mouse.get_pos()[1] - mouse_start_y
        pygame.draw.rect(game_display, WHITE, [mouse_start_x, mouse_start_y, w, h], 1)


def init_particles():
    create_particles(config.PARTICLE_NUMBER,
                     config.MIN_WIDTH + 10,
                     config.MAX_WIDTH - 10,
                     config.MIN_HEIGHT + 10,
                     config.MAX_HEIGHT - 10)


def create_particles(n, min_x, max_x, min_y, max_y):
    global grid
    bounds = [[config.MIN_WIDTH, config.MAX_WIDTH], [config.MIN_HEIGHT, config.MAX_HEIGHT]]
    grid = SpatialHashGrid(bounds, config.CELL_DIMENSIONS)

    particles.clear()
    for _ in range(n):
        x = randint(min_x, max_x)
        y = randint(min_y, max_y)
        add_particle(x, y)


def add_particle(x, y):
    i = len(particles)
    particle = Particle(i, x, y, config.PARTICLE_PARAMETERS)
    particles.append(particle)
    grid.add_particle(particle)


def draw_particles():
    width = config.MAX_WIDTH - config.MIN_WIDTH
    height = config.MAX_HEIGHT - config.MIN_HEIGHT
    grid.update_particles(particles)
    for p in particles:
        if p.id == 1:
            pygame.draw.circle(game_display, WHITE, (p.x, p.y), config.PARTICLE_PARAMETERS['r'], 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x + width, p.y), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x - width, p.y), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x, p.y + height), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x, p.y - height), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x + width, p.y + height), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x - width, p.y - height), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x + width, p.y - height), R, 1)
        #     pygame.draw.circle(game_display, WHITE, (p.x - width, p.y + height), R, 1)
        if config.DRAW_R_LINE:
            pygame.draw.circle(game_display, WHITE, (p.x, p.y), config.PARTICLE_PARAMETERS['r'], 1)
        pygame.draw.circle(game_display, p.color, (p.x, p.y), config.PARTICLE_RADIUS)

        p.step()
        grid.find_near(p)

    for p in particles:
        if p.x > config.MAX_WIDTH:
            p.x -= width
        elif p.x < config.MIN_WIDTH:
            p.x += width
        if p.y > config.MAX_HEIGHT:
            p.y -= height
        elif p.y < config.MIN_HEIGHT:
            p.y += height

    # if particles:
    #     for n in particles[1].nearby:
    #         n.color = (0, 0, 0)


def draw_limits():
    width = config.MAX_WIDTH - config.MIN_WIDTH
    height = config.MAX_HEIGHT - config.MIN_HEIGHT
    pygame.draw.rect(game_display, (100, 100, 100), [config.MIN_WIDTH, config.MIN_HEIGHT, width, height], 1)
    # pygame.draw.rect(game_display, (255, 0, 0), grid.get_cell_coordinates(2, 2), 1)


if __name__ == '__main__':
    main_loop()

pygame.quit()
quit()
