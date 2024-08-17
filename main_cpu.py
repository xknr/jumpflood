import pygame
import random
import numpy as np
import warnings
import math
import time

from jfa.jfasteps import JfaSteps

PIXEL_ID_NONE = 0x7fffffff
DISTANCE_INFINITE = 0x7fffffff

def coords2Id(x, y, w):
    return y * w + x

def calcDist(x, y, w, id):
    if id == PIXEL_ID_NONE:
        return DISTANCE_INFINITE
    return ((id % w) - x) ** 2 + ((id // w) - y) ** 2

def applyStep(pages, w, h, step):
    for j in range(h):
        for i in range(w):
            best, bestdist = PIXEL_ID_NONE, DISTANCE_INFINITE
            # Check 8 neighbors and self:
            for ny in range(j - step, j + step + 1, step):
                if ny < 0 or ny >= h: continue # Y outside canvas.
                for nx in range(i - step, i + step + 1, step):
                    if nx < 0 or nx >= w: continue # X outside canvas.
                    # if nx == i and ny == j: continue # Skip middle pixel.
                    src = pages[0][ny, nx] # Get neighbor's source pixel.
                    if src == PIXEL_ID_NONE: continue
                    srcdist = calcDist(i, j, w, src)
                    if srcdist < bestdist:
                        best, bestdist = src, srcdist
            pages[1][j, i] = best

# Convert src pixel info to color code.
def convertToPixels(pages, pixels, w, h):
    for j in range(h):
        for i in range(w):
            src = pages[0][j, i]
            if src == PIXEL_ID_NONE: 
                pixels[i, j] = (255, 0, 255)
            else:
                x, y = src % w, src // w
                r, g, b = x * 255 // w, y * 255 // h, 0
                pixels[i, j] = (r, g, b)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Perform an action when the space bar is pressed
                pass
    return True



def swapPages(pages):
    pages[0], pages[1] = pages[1], pages[0]


def placeRandomPoints(w, h, pages, numPoints):
    for i in range(numPoints):
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)
        pages[0][y, x] = coords2Id(x, y, w)




def main():

    # Treat warnings like errors (?)
    warnings.simplefilter('error')

    pygame.init()

    w, h = 200, 150
    #w, h = 400, 300

    surface = pygame.Surface((w, h))

    # Set the window size
    screen = pygame.display.set_mode((w, h))

    pages = [None] * 2
    for i in range(len(pages)):
        pages[i] = np.zeros((h, w), dtype=np.int32)

    currentStep = 0
    steps = None

    generators = [JfaSteps.jfa, JfaSteps.jfaIncreasing, JfaSteps.jfa1, JfaSteps.jfa2, JfaSteps._1jfa, JfaSteps.jfaPow2]
    currentSeed = 42 * len(generators)

    def reset():
        nonlocal steps, currentStep, currentSeed, generators

        random.seed(currentSeed // len(generators))
        pages[0].fill(PIXEL_ID_NONE)
        placeRandomPoints(w, h, pages, 30)

        maxStep = JfaSteps.calcMaxStep(w, h)
        steps = generators[0](maxStep)
        generators.append(generators.pop(0)) # remove from beginning, append to end
        currentStep = 0

        currentSeed += 1

        print(steps)


    firstReset = True

    # Game loop
    running = True
    while running:
        running = checkEvents()

        if not steps or currentStep >= len(steps):
            reset()
            if not firstReset:
                time.sleep(1)
            firstReset = False

        print("step =", steps[currentStep])
        applyStep(pages, w, h, steps[currentStep])
        currentStep += 1
        swapPages(pages)

        with pygame.pixelarray.PixelArray(surface) as pixels:
            convertToPixels(pages, pixels, w, h)

        screen.blit(surface, (0, 0))
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
