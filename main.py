from core.canvas import Canvas
from pygame import display
from core.recorder import *
from core.pen import Pen
import unicode
import pygame

pygame.init()
display.set_caption("vPaint")  # vectorPaint
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

canvas = Canvas()
# canvas.anti_aliasing = True

pen = Pen(canvas)
pen.color = 0x4caf50

recorder = Recorder(canvas)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            recorder.can_record = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == pygame.BUTTON_LEFT:
            recorder.can_record = recorder.protect_record = False
        elif e.type == pygame.KEYUP:
            if e.unicode == unicode.CTRL_Z:
                recorder.undo()
            elif e.unicode == unicode.CTRL_Y:
                recorder.redo()
            elif e.key == pygame.K_e:
                pass  # TODO: the eraser functional

    recorder.try_record(pygame.mouse.get_pos())

    surface.fill(0xffffff)

    canvas.render(surface)

    display.flip()
    clock.tick(60)
