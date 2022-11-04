from .canvas import Canvas


class Pen:
    def __init__(self, canvas: Canvas):
        # Config
        self.color = 0x000000
        self.size = 6

        # Other
        self.canvas = canvas
        self.canvas.pen = self

    def to_primitive(self):
        return {
            'color': self.color,
            'size': self.size
        }

    def apply_primitive(self, primitive: dict):
        self.color = primitive['color']
        self.size = primitive['size']


__all__ = 'Pen',
