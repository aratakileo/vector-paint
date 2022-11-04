from pygame.surface import SurfaceType


class CanvasError(Exception):
    def __init__(self, reason, *args):
        super().__init__(reason, *args)


class Canvas:
    def __init__(self):
        # Config
        self.anti_aliasing = False  # if enabled then impossible to set pen size

        # Data
        self.pen = None
        self.recorder = None
        self.project_manager = None

    def __check_components(self):
        if self.pen is None:
            raise CanvasError('pen component is not defined!')

        if self.recorder is None:
            raise CanvasError('recorder component is not defined!')

    def render(self, surface: SurfaceType):
        self.__check_components()
        self.recorder.render(surface)

    def to_primitive(self):
        self.__check_components()

        return {
            'pen': self.pen.to_primitive(),
            'points': self.recorder.to_primitive()
        }

    def apply_primitive(self, primitive: dict):
        self.pen.apply_primitive(primitive['pen'])
        self.recorder.apply_primitive(primitive['points'])


__all__ = 'CanvasError', 'Canvas'
