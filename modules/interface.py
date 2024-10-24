from .menu import Menu
from .level import Level

class MenuInterface:
    _menu: Menu

    def __init__(self, *, start_menu=None):
        self._menu = start_menu


    def add_start_menu(self, menu):
        self._menu = menu


    def get_menu(self):
        return self._menu


    async def next(self, num):
        next_menu = self._menu.menu_list()[num]
        next_menu.set_reader(self._reader)
        await next_menu.run()
        if next_menu.menu_list():
            self._menu = next_menu


    async def back(self):
        prev_menu = self._menu.get_parent()
        prev_menu.set_reader(self._reader)
        await self._menu.on_escape()
        if prev_menu:
            self._menu = prev_menu

    def set_reader(self, reader):
        self._reader = reader
        self._menu.set_reader(reader)

