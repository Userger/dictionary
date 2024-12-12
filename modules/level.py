from .menu import Menu, EscapeMenu
from .gameprocess import GameProcess
from .exceptions import Escape
from random import randrange
from settings import DICT_DIR
from pathlib import Path

class EmptyDict(Exception):
    pass

class Level(Menu):
    def __init__(self,
         title, *,
         range_start=0,
         range_num=None,
         duration=None,
         amount=None,
         dictionary = None
     ):
        super().__init__(title)
        self._range_start: int = range_start or 0
        self._range_num: int | None = range_num or None
        self._amount: int | None = amount or None
        self._dictionary: set | tuple | list | dict = dictionary
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

    def _get_dict(self) -> list | tuple:
        if isinstance(self._dictionary, dict):
            return tuple(self._dictionary.items())
        elif isinstance(self._dictionary, (list, tuple)):
            return self._dictionary
        elif isinstance(self._dictionary, set):
            return tuple(self._dictionary)

        lines = self._load_lines()
        cliped = self._clip_lines(lines)
        randomlines = self._random_lines(cliped)
        result = tuple(map(self._line_to_tuple, randomlines))
        return result


    async def on_escape(self):
        self._menu_list = []


    async def run(self):
        await self._start()


    def _load_lines(self) -> list[str]:
        mode = self._parent.get_parent().title
        dct = self._parent.title
        with open(Path(DICT_DIR) / mode / dct) as f:
            return f.readlines()


    def _random_lines(self, lines: list[tuple[str, tuple[str]]]) -> set[tuple[str, tuple[str]]]:
        if not self._amount or self._amount > len(lines):
            return lines

        result = set()
        while len(result) < min(self._amount, len(lines)):
            num = randrange(0, len(lines))
            result.add(lines[num])
        return result


    def _line_to_tuple(self, line: str) -> tuple[str, tuple[str]]:
        eng, ru = line.split('=')
        ru = tuple(map(lambda w: w.strip(), ru.split(',')))
        return (eng.strip(), ru)


    def _clip_lines(self, lines: list) -> list:
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
        self._dir: str = dir
        self._filename: str = title
    def _load_lines(self) -> list[str]:
        with open(f"dicts/{self._dir}/{self._filename}") as f:
            return f.readlines()

