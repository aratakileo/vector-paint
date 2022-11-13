from projectmanager import ProjectManager
from core.canvas import Canvas
from pygex.input import Input
from pygex.mouse import Mouse
from core.recorder import *
from pygame import display
from core.pen import Pen
import pygame


pygame.init()
display.set_caption("vPaint")  # vectorPaint
display.set_mode((800, 800), pygame.RESIZABLE)

surface = display.get_surface()
clock = pygame.time.Clock()

mouse = Mouse()
input = Input()

canvas = Canvas()
# canvas.antialiasing = True

pen = Pen(canvas)
pen.color = 0x4caf50

recorder = Recorder(canvas)

project_manager = ProjectManager(canvas)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        input.process_event(e)
        mouse.process_event(e)

    if mouse.left_is_up:
        recorder.protect_record = False

    recorder.can_record = mouse.left_is_hold

    if input.is_hold(Input.GK_CTRL):
        if input.is_applying(pygame.K_z):
            recorder.undo()
        elif input.is_applying(pygame.K_y):
            recorder.redo()
        elif input.is_up(pygame.K_s):
            project_manager.save()
        elif input.is_up(pygame.K_l):
            project_manager.load()

    recorder.try_record(pygame.mouse.get_pos())

    surface.fill(0xffffff)

    canvas.render(surface)

    display.flip()
    input.flip()
    mouse.flip()
    clock.tick(60)
