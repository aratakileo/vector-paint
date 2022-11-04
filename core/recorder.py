from pygame.draw import lines as draw_lines, circle as draw_circle, aalines as draw_aalines
from pygame.surface import SurfaceType
from typing import Sequence
from .canvas import *
from .pen import Pen


class Recorder:
    def __init__(self, canvas: Canvas):
        # Config
        self.segment_limit = 100  # max count of points at segment

        # Other
        self.canvas = canvas
        self.canvas.recorder = self

        if self.canvas.pen is None:
            raise CanvasError('need to create pen firstly')

        self.can_record = self.protect_record = False

        self.segments = [Segment(self.canvas.pen)]
        self.redo_segments = []

    def record(self, point: Sequence):
        if not self.can_record or self.protect_record:
            return

        segment = self.segments[-1]

        segment.append_point(point, self.canvas.pen)
        self.clear_redo_data()

        if len(segment.points) == self.segment_limit:
            self.abort_segment(point)

    def stop_record(self):
        if not self.segments[-1].is_empty():
            self.abort_segment()

        # needs for situation when reached segment limit and next segment is empty
        if len(self.segments) >= 2 and len(self.segments[-1].points) == 1 \
                and self.segments[-2].points[-1] == self.segments[-1].points[-1]:
            self.segments[-1].points.clear()

        if self.can_record:
            self.protect_record = True

    def try_record(self, pos: Sequence):
        if self.can_record:
            self.record(pos)
        else:
            self.stop_record()

    def undo(self):
        if len(self.segments) <= 1:
            return

        self.stop_record()

        self.redo_segments.insert(0, self.segments[-2])
        del self.segments[-2]

    def redo(self):
        if not self.redo_segments:
            return

        self.stop_record()

        del self.segments[-1]

        recovery_segment = self.redo_segments[0]
        self.segments.append(recovery_segment)
        self.canvas.pen.color = recovery_segment.color
        self.canvas.pen.size = recovery_segment.size

        del self.redo_segments[0]

    def clear_redo_data(self):
        self.redo_segments = []

    def abort_segment(self, prev_point: Sequence = None):
        self.segments.append(Segment(self.canvas.pen, prev_point))

    def render(self, surface: SurfaceType):
        for segment in self.segments:
            segment.render(surface, self.canvas.antialiasing)

    def to_primitive(self):
        return [segment.to_primitive() for segment in self.segments[:-1]]

    def apply_primitive(self, primitive: list):
        self.clear_redo_data()
        self.segments = [
                            Segment.from_primitive(
                                primitive_segment,
                                self.canvas.pen
                            ) for primitive_segment in primitive
                        ] + [Segment(self.canvas.pen)]


class Segment:
    def __init__(self, pen: Pen, prev_point: Sequence = None):
        self.color, self.size = pen.color, pen.size

        self.points = [] if prev_point is None else [prev_point]

    @staticmethod
    def from_primitive(primitive: dict, pen: Pen):
        segment = Segment(pen)
        segment.color = primitive['color']
        segment.size = primitive['size']
        segment.points = primitive['points']

        return segment

    def is_empty(self):
        return not self.points

    def append_point(self, point: Sequence, pen: Pen):
        if self.points and self.points[-1] == point:
            return

        self.color, self.size = pen.color, pen.size
        self.points.append(point)

    def render(self, surface: SurfaceType, antialiasing=False):
        if len(self.points) >= 2:
            if antialiasing:
                draw_aalines(surface, self.color, False, self.points, self.size)
                return

            draw_lines(surface, self.color, False, self.points, self.size)
        elif len(self.points) == 1:
            draw_circle(surface, self.color, self.points[0], self.size / 2)

    def to_primitive(self):
        return {
            'color': self.color,
            'size': self.size,
            'points': self.points
        }


__all__ = 'Recorder', 'Segment'
