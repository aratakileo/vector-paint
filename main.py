from pygame.constants import K_z, K_l, K_s, K_F1, K_F11
from projectmanager import ProjectManager
from pygex.color import GREEN, WHITE
from core.recorder import Recorder
from pygex.gui.toast import Toast
from core.canvas import Canvas
from pygex.input import Input
from core.pen import Pen
from pygex import Window


window = Window(title='VectorPaint')
window.bg_color = WHITE
window.fps_limit = 120

fullscreen_toast = Toast('To exit full screen press [F11]')

canvas = Canvas()
pen = Pen(canvas)
pen.color = GREEN

recorder = Recorder(canvas)
project_manager = ProjectManager(canvas)

while True:
    if window.mouse.left_is_up:
        recorder.protect_record = False

    recorder.can_record = window.mouse.left_is_hold

    if window.input.is_hold(Input.GK_CTRL):
        if window.input.is_applying(K_z):
            if window.input.is_hold(Input.GK_SHIFT):
                recorder.redo()
            else:
                recorder.undo()
        elif window.input.is_up(K_s):
            project_manager.save()
            window.show_toast('Project saved!')
        elif window.input.is_up(K_l):
            project_manager.load()
            window.show_toast('Project loaded!')
    elif window.input.is_up(K_F11):
        window.fullscreen = not window.fullscreen

        if window.fullscreen:
            fullscreen_toast.show()
        else:
            fullscreen_toast.cancel()

    recorder.try_record(window.mouse.pos)

    canvas.render(window.surface)

    if window.input.is_up(K_F1):
        window.take_screenshot()

    window.flip()
