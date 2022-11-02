from pygame.draw import lines as draw_lines, circle as draw_circle
from pygame.surface import SurfaceType
from typing import Sequence


class Recorder:
    def __init__(self):
        self.can_record = self.protect_record = False

        self.pen = Pen(self)

        self.segments = [Segment(self.pen)]
        self.segments_recovery = []

    def record(self, point: Sequence):
        if not self.can_record or self.protect_record:
            return

        segment = self.segments[-1]

        segment.append_point(point, self.pen)
        self.segments_recovery = []

        if len(segment.points) == self.pen.segment_limit:
            self.abort_segment(point)

    def stop_record(self):
        if not self.segments[-1].is_empty():
            self.abort_segment()

        self.segments[-1].prev_point = None  # needs for situation when reached segment limit and next segment is empty

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

        self.segments_recovery.insert(0, self.segments[-2])
        del self.segments[-2]

    def redo(self):
        if not self.segments_recovery:
            return

        self.stop_record()

        del self.segments[-1]

        self.segments.append(self.segments_recovery[0])
        del self.segments_recovery[0]

    def abort_segment(self, prev_point: Sequence = None):
        self.segments.append(Segment(self.pen, prev_point))


class Pen:
    def __init__(self, recorder: Recorder):
        self.recorder = recorder
        self.recorder.pen = self

        self.segment_limit = 100  # max count of points at segment
        self.color = 0x000000
        self.size = 6

    def render(self, surface: SurfaceType):
        for segment in self.recorder.segments:
            segment.render(surface)


class Segment:
    def __init__(self, pen: Pen, prev_point: Sequence = None):
        self.color, self.size = pen.color, pen.size
        self.prev_point = prev_point

        self.points = []

    def is_empty(self):
        return not self.points

    def append_point(self, point: Sequence, pen: Pen):
        if self.points and self.points[-1] == point:
            return

        if self.prev_point == point:
            self.prev_point = None

        self.color, self.size = pen.color, pen.size
        self.points.append(point)

    def render(self, surface: SurfaceType):
        points = self.points

        if self.prev_point is not None:
            points.insert(0, self.prev_point)
            print(self.prev_point)

        if len(points) >= 2:
            draw_lines(surface, self.color, False, points, self.size)
        elif len(points) == 1:
            draw_circle(surface, self.color, points[0], self.size / 2)


__all__ = (
    'Pen',
    'Recorder',
    'Segment'
)
