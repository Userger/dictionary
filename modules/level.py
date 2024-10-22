from .menu import Menu, EscapeMenu
from .gameprocess import GameProcess
from .exceptions import Escape
from random import randrange
from settings import COMMON_DICT_DIRS, SELF_DICT_DIRS

class EmptyDict(Exception):
    pass

class Level(Menu):
    def __init__(self, title, *,
                 range_start=0,
                 range_num=None,
                 duration=60,
                 amount=None):
        super().__init__(title)
        self._range_start = range_start
        self._range_num = range_num
        self._amount = amount
        self._opts = {
            'duration': duration,
            'dictionary': None,
        }


    async def _start(self):
        try:
            self._opts['dictionary'] = self._get_dict()
            gameprocess = GameProcess(**self._opts)
            results = await gameprocess.start()
            self._menu_list = [
                Menu(f'exited: {results["exited"]}'),
                Menu(f'points: {results["points"]}'),
                Menu(f'fails: {results["fails"]}'),
                EscapeMenu('back'),
            ]
        except EmptyDict:
            self._menu_list = [
                Menu(f'empty dictionary:  INCORRECT level settings!'),
                EscapeMenu('back'),
            ]

    def _get_dict(self):
        lines = self._load_lines()
        cliped = self._clip_lines(lines)
        randomlines = self._random_lines(cliped)
        result = tuple(map(self._line_to_tuple, randomlines))
        return result


    async def on_escape(self):
        self._menu_list = []


    async def run(self):
        await self._start()


    def _load_lines(self):
        mode = self._parent.title
        if mode == 'common':

            if self._range_start <= 1000:
                with open(COMMON_DICT_DIRS[0]) as f:
                    return f.readlines()

            elif self._range_start <= 2000:
                self._range_start = self._range_start - 1000
                with open(COMMON_DICT_DIRS[1]) as f:
                    return f.readlines()

        elif mode == 'dict':
            with open(SELF_DICT_DIRS[0]) as f:
                return f.readlines()


    def _random_lines(self, lines):
        if not self._amount:
            return lines

        result = set()
        while len(result) < min(self._amount, len(lines)):
            num = randrange(0, len(lines))
            result.add(lines[num])
        return result


    def _line_to_tuple(self, line):
        eng, ru = line.split('=')
        ru = tuple(map(lambda w: w.strip(), ru.split(',')))
        return (eng.strip(), ru)


    def _clip_lines(self, lines):
        cliped = lines[self._range_start:][:self._range_num]
        if not cliped:
            raise EmptyDict()
        return cliped
