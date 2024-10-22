from .exceptions import Escape, Exit

class Menu:
    def __init__(self, title):
        self.title = title
        self._menu_list = []
        self._parent = None

    def add_submenu(self, *menu_list):
        for menu in menu_list:
            menu.set_parent(self)
        self._menu_list.extend(menu_list)

    def menu_list(self):
        return self._menu_list

    def set_parent(self, menu):
        self._parent = menu

    def get_parent(self):
        return self._parent


    # calling when menu has no menu_list
    async def run(self):
        pass
    # calling when menu has no parent
    async def on_escape(self):
        pass


class ExitMenu(Menu):
    async def run(self):
        raise Exit()

class EscapeMenu(Menu):
    async def run(self):
        raise Escape()
