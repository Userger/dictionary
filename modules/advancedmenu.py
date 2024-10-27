import os
import sys
import asyncio
import importlib
import settings.settings
from .menu import InputMenu, Menu
from settings.util import change_setting
from .exceptions import Escape
from .level import Level

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


class CustomLevelMenu(InputMenu):
    async def run(self):
        opts_dict = {
            "range_start": None,
            "range_num": None,
            "duration": None,
            "amount": None,
        }
        opts: list = []
        message = \
        'enter options divide by " "\n' \
        'to skip option write "-"\n' \
        'order:    range_start range duration amount\n' \
        'defaults: 0           all   60       all'

        self._clear()
        print(message)

        try:
            while string := (await self._read()).strip():
                try:
                    opts = self._get_opts_list(string)
                    if len(opts) > len(opts_dict):
                        raise ValueError()
                    break
                except ValueError:
                    sys.stdout.write('\033[G')
                    sys.stdout.write('\033[K')
                    asyncio.create_task(self. \
                            _incorrect_message())
                    continue

            for opt, key in zip(opts, opts_dict):
                opts_dict[key] = opt
            level = Level('start', **opts_dict)
            level.set_parent(self._parent)
            level.set_reader(self._reader)
            self._menu_list = [level]
        except Escape:
            self._menu_list = []


    def _get_opts_list(self, string):
        opts = []
        for opt in string.split(' '):
            if not opt:
                continue
            elif opt.strip() == '-':
                opts.append(None)
            else:
                opts.append(int(opt))
        return opts

    async def _incorrect_message(self):
        sys.stdout.write('\0337')
        sys.stdout.write('\033[B')
        sys.stdout.write('\033[G')
        sys.stdout.write('Incorrect opts!!!')
        sys.stdout.write('\0338')
        sys.stdout.flush()
        await asyncio.sleep(2)
        sys.stdout.write('\0337')
        sys.stdout.write('\033[B')
        sys.stdout.write('\033[2K')
        sys.stdout.write('\0338')
        sys.stdout.flush()


