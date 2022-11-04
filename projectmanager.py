from core.canvas import Canvas
from json import dumps, loads


class ProjectManagerError(Exception):
    def __init__(self, reason, *args):
        super().__init__(reason, *args)


class ProjectManager:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas.project_manager = self

    @property
    def ver(self):
        return 'vpaint-alpha-1'

    @property
    def extension(self):
        return 'vpaint'

    def is_ver_support(self, ver: str):
        return self.ver == ver

    def dumps(self):
        result = f'ver:{self.ver};'

        return result + dumps({'canvas': self.canvas.to_primitive()})

    def save(self):
        self.canvas.recorder.stop_record()

        with open(f'project.{self.extension}', 'w', encoding='utf-8') as f:
            f.write(self.dumps())

    def load(self):
        with open(f'project.{self.extension}', 'r', encoding='utf-8') as f:
            any_str = f.read()

        head_ending_index = -1
        for char in any_str:
            head_ending_index += 1

            if char == ';':
                break

        metadata = any_str[:head_ending_index].split(':')

        if metadata[0] != 'ver':
            raise ProjectManagerError('the project file is corrupted')

        if not self.is_ver_support(metadata[1]):
            raise ProjectManagerError('this project version is not support!')

        self.canvas.recorder.stop_record()
        self.canvas.apply_primitive(loads(any_str[head_ending_index + 1:])['canvas'])
