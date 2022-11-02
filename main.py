from pygame import display
from pen import *
import unicode
import pygame

pygame.init()
display.set_caption("upaint")
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

recorder = Recorder()
pen = Pen(recorder)
pen.color = 0x4caf50

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

    recorder.try_record(pygame.mouse.get_pos())

    surface.fill(0xffffff)

    pen.render(surface)

    display.flip()
    clock.tick(60)
