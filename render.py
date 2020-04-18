import board
import neopixel


def convert(array):
    monodimensional_array = []
    for i in range(0, 16):
        if i % 2 == 0:
            for j in array[i]:
                monodimensional_array.append(j)   
        else:
            for j in array[i][::-1]:
                monodimensional_array.append(j)
    return monodimensional_array


def show(array):
    pixels = neopixel.NeoPixel(board.D18, 256, auto_write=False)

    array = convert(array[:])
    for i in range(0, 256):
        pixels[i] = array[i]

    pixels.show()
