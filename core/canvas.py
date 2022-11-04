from pygame.surface import SurfaceType


class CanvasError(Exception):
    def __init__(self, reason, *args):
        super().__init__(reason, *args)


class Canvas:
    def __init__(self):
        # Config
        self.anti_aliasing = False  # if enabled then impossible to set pen size

        # Data
        self.recorder = None
        self.pen = None

    def __check_components(self):
        if self.pen is None:
            raise CanvasError('pen component is not defined!')

        if self.recorder is None:
            raise CanvasError('recorder component is not defined!')

    def render(self, surface: SurfaceType):
        self.__check_components()
        self.recorder.render(surface)


__all__ = 'CanvasError', 'Canvas'
