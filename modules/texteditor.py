import os
from .menu import Menu
from settings.settings import TEXT_EDITOR
class TextEditorMenu(Menu):
    def __init__(self, title, dir=None):
        super().__init__(title)
        if not dir:
            self.title = 'Error: bad menu args!'
        self._dir = dir
    async def run(self):
        if not self._dir:
            return
        os.system(f'{TEXT_EDITOR} {self._dir}')

