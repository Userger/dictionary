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
                 duration=None,
                 amount=None,
                 dictionary = None):
        super().__init__(title)
        self._range_start = range_start or 0
        self._range_num = range_num or None
        self._amount = amount or None
        self._dictionary = dictionary
        self._opts = {
            'duration': duration or 60,
            'dictionary': None,
        }


    async def _start(self):
        try:
            self._opts['dictionary'] = self._get_dict()
            gameprocess = GameProcess(self._reader, **self._opts)
            results = await gameprocess.start()


            self._menu_list = [
                EscapeMenu('back'),
                Menu(''),
                Menu('Results:'),
                Menu(f'exited: {results["exited"]}'),
                Menu(f'points: {results["points"]}'),
                Menu(f'fails: {results["fails"]}'),
            ]

            if results["fails"]:
                fails_level = Level('play with fails',
                    dictionary=results['failed_words'])
                fails_level.set_parent(self._parent)
                self._menu_list.insert(0, fails_level)

        except EmptyDict:
            self._menu_list = [
                Menu(f'empty dictionary:  INCORRECT level settings!'),
                EscapeMenu('back'),
            ]

    def _get_dict(self):
        if isinstance(self._dictionary, dict):
            return tuple(self._dictionary.items())
        elif isinstance(self._dictionary, (list, tuple)):
            return self._dictionary

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

            if self._range_start < 1000:
                with open(COMMON_DICT_DIRS[0]) as f:
                    return f.readlines()

            elif self._range_start < 2000:
                self._range_start = self._range_start - 1000
                with open(COMMON_DICT_DIRS[1]) as f:
                    return f.readlines()

        elif mode == 'dict':
            with open(SELF_DICT_DIRS[0]) as f:
                return f.readlines()


    def _random_lines(self, lines):
        if not self._amount or self._amount > len(lines):
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

class DirLevel(Level):
    def __init__(self, title, dir, subtitle='', *,
                 range_start=0,
                 range_num=None,
                 duration=60,
                 amount=None):
        super().__init__(title + ' ' + subtitle,
                         range_start=range_start,
                         range_num=range_num,
                         duration=duration,
                         amount=amount)
        self._dir = dir
        self._filename = title
    def _load_lines(self):
        with open(f"dicts/{self._dir}/{self._filename}") as f:
            return f.readlines()

