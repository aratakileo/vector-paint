from pygame.draw import lines as draw_lines, circle as draw_circle
from pygame.surface import SurfaceType
from typing import Sequence


class Recorder:
    def __init__(self):
        self.segment_limit = 100  # max count of points at segment
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

        self.segments_recovery.insert(0, self.segments[-2])
        del self.segments[-2]

    def redo(self):
        if not self.segments_recovery:
            return

        self.stop_record()

        del self.segments[-1]

        recovery_segment = self.segments_recovery[0]
        self.segments.append(recovery_segment)
        self.pen.color = recovery_segment.color
        self.pen.size = recovery_segment.size

        del self.segments_recovery[0]

    def abort_segment(self, prev_point: Sequence = None):
        self.segments.append(Segment(self.pen, prev_point))


class Pen:
    def __init__(self, recorder: Recorder):
        self.recorder = recorder
        self.recorder.pen = self

        self.color = 0x000000
        self.size = 6

    def render(self, surface: SurfaceType):
        for segment in self.recorder.segments:
            segment.render(surface)


class Segment:
    def __init__(self, pen: Pen, prev_point: Sequence = None):
        self.color, self.size = pen.color, pen.size

        self.points = [] if prev_point is None else [prev_point]

    def is_empty(self):
        return not self.points

    def append_point(self, point: Sequence, pen: Pen):
        if self.points and self.points[-1] == point:
            return

        self.color, self.size = pen.color, pen.size
        self.points.append(point)

    def render(self, surface: SurfaceType):
        if len(self.points) >= 2:
            draw_lines(surface, self.color, False, self.points, self.size)
        elif len(self.points) == 1:
            draw_circle(surface, self.color, self.points[0], self.size / 2)


__all__ = (
    'Pen',
    'Recorder',
    'Segment'
)
