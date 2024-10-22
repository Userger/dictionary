import asyncio
import tty
import sys
import os
from .menu import Menu
from .util import create_stdin_reader
from .interface import MenuInterface
from .exceptions import Exit, Escape

class DrawMenu:
    _reader: asyncio.StreamReader
    _interface: MenuInterface
    def __init__(self, interface: MenuInterface):
        self._interface = interface


    def _draw_menu_list(self, menu_list):
        coords = []
        os.system('clear')

        for i, menu in enumerate(menu_list):
            coords.append(f'{i+1};1')
            sys.stdout.write(f'\033[{coords[i]}H')
            sys.stdout.write(menu.title)
        sys.stdout.flush()

        return coords


    async def start(self):
        tty.setcbreak(sys.stdout)
        os.system('clear')

        while True:
            try:
                self._reader = await create_stdin_reader()
                menu_list = self._interface.get_menu().menu_list()
                coords = self._draw_menu_list(menu_list)
                num = await self.get_menu_num(coords)
                await self._interface.next(num)

            except Exit:
                break
            except Escape:
                await self._interface.back()


    async def get_menu_num(self, coords):
        cursor_pos = 0
        def move_cursor():
            sys.stdout.write(f'\033[{coords[cursor_pos]}H')
            sys.stdout.flush()
        move_cursor()

        while (diraction := await self._reader.read(4)) != b'\n':

            if diraction in (b'j', b'w', b'J', b'W',) \
              and cursor_pos<len(coords)-1:
                cursor_pos += 1
                move_cursor()

            elif diraction in (b'k', b'r', b'K', b'R',) \
              and cursor_pos>0:
                cursor_pos -= 1
                move_cursor()

            elif diraction == b'\x1B':
                raise Escape()

        return cursor_pos

