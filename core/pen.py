from .canvas import Canvas


class Pen:
    def __init__(self, canvas: Canvas):
        # Config
        self.color = 0x000000
        self.size = 6

        # Other
        self.canvas = canvas
        self.canvas.pen = self


__all__ = 'Pen',
