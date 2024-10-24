from .menu import InputMenu
from settings.util import change_setting

class NewTextEditorMenu(InputMenu):
    async def run(self):
        self._clear()
        print('Enter name of your text editor and press Enter.')
        res = (await self._read()).strip()
        self.title = res
        change_setting('TEXT_EDITOR', res)
