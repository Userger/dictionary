from .exceptions import Escape, Exit
from asyncio import StreamReader
import sys
import os

class Menu:
    def __init__(self, title):
        self.title: str = title
        self._menu_list: list[Menu] = []
        self._parent: Menu | None = None

    def add_submenu(self, *menu_list):
        for menu in menu_list:
            menu.set_parent(self)
        self._menu_list.extend(menu_list)
        return self

    def menu_list(self):
        return self._menu_list

    def set_parent(self, menu):
        self._parent = menu

    def get_parent(self):
        return self._parent

    def set_reader(self, reader: StreamReader):
        self._reader = reader

    # Abstract
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


class InputMenu(Menu):
    def _clear(self):
        os.system('clear')
    async def _read(self) -> str:
        chars = []
        while (char := await self._reader.read(4)) != b'\n':
            if char == b'\x7F' and chars:
                chars.pop()
                sys.stdout.write('\033[D')
                sys.stdout.write(' ')
                sys.stdout.write('\033[D')
                sys.stdout.flush()
            elif char == b'\x1B':
                raise Escape()
            else:
                char = char.decode()
                chars.append(char)
                sys.stdout.write(char)
                sys.stdout.flush()

        string = ''.join(chars)
        return string

    async def run(self):
        res = await self._read()

