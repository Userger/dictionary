import os
import importlib
import settings.settings
from .menu import Menu
class TextEditorMenu(Menu):
    def __init__(self, title, dir=None):
        super().__init__(title)
        if not dir:
            self.title = 'Error: bad menu args!'
        self._dir = dir
    async def run(self):
        importlib.reload(settings.settings)
        if not self._dir:
            return
        os.system(f'{settings.settings.TEXT_EDITOR} {self._dir}')

