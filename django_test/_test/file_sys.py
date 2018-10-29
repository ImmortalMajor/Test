from pathlib import Path
from configparser import ConfigParser
import os
import platform
import string


class FileSys:
    def __init__(self):
        cp = ConfigParser()
        file = os.path.join(os.path.dirname(__file__), 'path.ini')
        cp.read(file)
        path = cp['DEFAULT']['path']
        self.path = Path(path)

    def go_to(self, dir):
        sub_dir = self.path / dir
        if dir == '..':
            if list(self.path.parents):
                self.path = self.path.parents[0]
        elif sub_dir.exists() and sub_dir.is_dir():
            self.path = sub_dir
        return self.get_content()

    def get_content(self):
        return {
            'path': str(self.path),
            'drives': list(string.ascii_uppercase) if platform.system() == 'Windows' else [],
            'folders': list(folder.name for folder in self.path.iterdir() if folder.is_dir()),
            'images': list(image.name
                           for image in self.path.iterdir()
                           if image.suffix in ['.img', '.png', '.jpg', '.bmp'])
        }

