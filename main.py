import pygame
import time
import random
import neopixel
import board


pixels = neopixel.NeoPixel(board.D18, 256, auto_write=False)
initial_y, initial_x = 0, 7


def main(game_field):
    figure_index = random.randint(0, 4)
    figure_rotation = random.randint(0, 3)
    y, x = initial_y, initial_x
    figure = get_figure(figure_index, figure_rotation, y, x, get_color())
    game_field = update_game_field(game_field[:], figure)
    render(game_field[:])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 3:
                    if not x_stop(game_field, figure, 'left'):
                        figure = update_figure(figure[:], 0, -1)
                if event.button == 1:
                    if not  x_stop(game_field, figure, 'right'):
                        figure = update_figure(figure[:], 0, 1)
                if event.button == 9:
                    pause()
                if event.button == 10:
                    start_and_stop()

        if not y_stop(game_field, figure, y):
            game_field = update_game_field(game_field[:], figure)
            render(game_field[:])
            no_figure = get_no_figure(figure[:])
            game_field = update_game_field(game_field[:], no_figure)
            time.sleep(0.2)
            figure = update_figure(figure[:], 1, 0)
            y += 1
        else:
            y = 0
            figure = update_figure(figure[:], 0, 0)
            game_field = update_game_field(game_field[:], figure)
            render(game_field[:])
            lines = full_lines(game_field)
            if lines != []:
                game_field = del_full_lines(game_field[:], lines)
                render(game_field[:])

            y, x = initial_y, initial_x
            figure_index = random.randint(0, 4)
            figure_rotation = random.randint(0, 3)
            figure = get_figure(figure_index, figure_rotation, y, x, get_color())

def get_color():
    r = random.randint(0, 25)
    g = random.randint(0, 25)
    b = random.randint(0, 25)
    return (r, g, b)


def full_lines(game_field):
    lines = []

    for i in range(0, 16):
        if all(x != (0, 0, 0) for x in game_field[i]):
            lines.append(i)

    return lines

def del_full_lines(game_field, lines):

    for i in lines:
        del game_field[i]
        game_field.insert(0, [(0, 0, 0) for j in range(0, 16)])

    return game_field


def x_stop(game_field, figure, direction):
    for i in figure[0]:
        if direction == 'left':
            if i[1] - 1 < 0 or game_field[i[0]][i[1] - 1] != (0, 0, 0):
                return True
        if direction == 'right':
            if i[1] + 1 > 15 or game_field[i[0]][i[1] + 1] != (0, 0, 0):
                return True
    return False


def y_stop(game_field, figure, y):
    for i in figure[0]:
        if i[0] + 1 > 15 or (game_field[i[0] + 1][i[1]] != (0, 0, 0) and y != 0):
            return True
    return False


def update_figure(figure, y, x):
    for i in range(0, 4):
        figure[0][i][0] += y
        figure[0][i][1] += x
    return figure


def get_no_figure(figure):
    figure[1] = (0, 0, 0)
    return figure


def update_game_field(game_field, figure):
    for i in range(0, 4):
        game_field[figure[0][i][0]][figure[0][i][1]] = figure[1]
    return game_field


def get_figure(figure, rotation, y, x, color):
    figures = (
            ([[0, 0], [0, 1], [0, 2], [0, 3]], [[0, 0], [1, 0], [2, 0], [3, 0]], [[0, 0], [0, 1], [0, 2], [0, 3]], [[0, 0], [1, 0], [2, 0], [3, 0]]), 
            ([[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]]),
            ([[0, 1], [1, 0], [1, 1], [1, 2]], [[0, 0], [1, 0], [1, 1], [2, 1]], [[0, 0], [0, 1], [0, 2], [1, 1]], [[0, 1], [1, 0], [1, 1], [2, 1]]),
            ([[0, 1], [1, 0], [1, 1], [2, 1]], [[0, 0], [0, 1], [1, 1], [1, 2]], [[0, 1], [1, 0], [1, 1], [2, 1]], [[0, 0], [0, 1], [1, 1], [1, 2]]),
            ([[0, 0], [1, 0], [2, 0], [2, 1]], [[0, 0], [0, 1], [0, 2], [1, 0]], [[0, 0], [0, 1], [1, 1], [2, 1]], [[0, 2], [1, 0], [1, 1], [1, 2]]),
        )
    needed_figure = [figures[figure][rotation], color]

    for i in range(0, 4):
        needed_figure[0][i][0] += y 
        needed_figure[0][i][1] += x

    return needed_figure[:]


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    return


def start_and_stop():
    game_field = [[(0, 0, 0) for i in range(0, 16)] for j in range(0, 16)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 10:
                    main(game_field[:])
                    print(event.button)


def convert(array):
    monoarray = []
    for i in range(0, 16):
        for j in range(0, 16):
            if i % 2 == 0:
                monoarray.append(array[j][i])
            else:
                monoarray.append(array[::-1][j][i])
    return monoarray


def render(array):
    monoarray = convert(array[:])
    for i in range(0, 256):
        pixels[i] = monoarray[i]
    pixels.show()


def init():
    pygame.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()
    axis = {}
    button = {}

    start_and_stop()


if __name__ == '__main__':
    init()
