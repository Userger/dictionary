import os
import importlib
import settings.settings
from .menu import InputMenu, Menu
from settings.util import change_setting

class NewTextEditorMenu(InputMenu):
    async def run(self):
        self._clear()
        print('Enter name of your text editor and press Enter.')
        res = (await self._read()).strip()
        self.title = res
        change_setting('TEXT_EDITOR', res)


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

