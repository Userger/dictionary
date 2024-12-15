from pathlib import Path
from random import randrange

from settings import DICT_DIR

from .gameprocess import GameProcess, GameResult
from .menu import EscapeMenu, Menu


class EmptyDict(Exception):
    pass


class Level(Menu):

    def __init__(
        self,
        title,
        *,
        range_start=0,
        range_num=None,
        duration=None,
        amount=None,
        dictionary=None,
        constraint=None,
    ):
        super().__init__(title)
        self._range_start: int = range_start or 0
        self._range_num: int | None = range_num or None
        self._amount: int | None = amount or None
        self._dictionary: list[tuple[str, list[str]]] | None = dictionary
        self._opts = {
            "amount": constraint,
            "duration": duration if constraint or duration else 60,
        }

    async def run(self):
        await self._start()

    async def on_escape(self):
        self._menu_list = []

    async def _start(self):
        try:
            self._opts["dictionary"] = self._get_dict()
            gameprocess = GameProcess(self._reader, **self._opts)
            result: GameResult = await gameprocess.run()

            self._menu_list = [
                EscapeMenu("back"),
                Menu(""),
                Menu("Results:"),
                Menu(f"exited: {result.exited}"),
                Menu(f"points: {result.points}"),
                Menu(f"fails: {result.fails}"),
            ]

            if fails := result.fails:
                constraint = fails * 5
                fails_level = Level(
                    "play with fails",
                    dictionary=list(result.failed_words.items()),
                    constraint=constraint,
                )
                fails_level.set_parent(self._parent)
                self._menu_list.insert(0, fails_level)

        except EmptyDict:
            self._menu_list = [
                Menu("empty dictionary:  INCORRECT level settings!"),
                EscapeMenu("back"),
            ]

    def _get_dict(self) -> list[tuple[str, list[str]]]:
        if self._dictionary:
            return self._dictionary

        lines = self._read_lines_from_dict_file()
        cliped_lines = self._clip_lines(lines)
        random_lines = self._random_lines(cliped_lines)
        list_of_tuples_dict = self._lines_to_tuple_list(random_lines)
        return list_of_tuples_dict

    def _lines_to_tuple_list(self, lines: list[str]) -> list[tuple[str, list[str]]]:
        return list(map(self._line_to_tuple, lines))

    def _read_lines_from_dict_file(self) -> list[str]:
        mode = self._parent.get_parent().title
        dct = self._parent.title
        with open(Path(DICT_DIR) / mode / dct) as f:
            return f.readlines()

    def _random_lines(self, lines: list[str]) -> list[str]:
        if not self._amount or self._amount > len(lines):
            return lines

        result = set()
        while len(result) < min(self._amount, len(lines)):
            num = randrange(0, len(lines))
            result.add(lines[num])
        return list(result)

    def _line_to_tuple(self, line: str) -> tuple[str, list[str]]:
        eng, ru = line.split("=")
        ru = list(map(lambda w: w.strip(), ru.split(",")))
        return eng.strip(), ru

    def _clip_lines(self, lines: list[str]) -> list[str]:
        cliped = lines[self._range_start :][: self._range_num]
        if not cliped:
            raise EmptyDict()
        return cliped


class DirLevel(Level):
    def __init__(
        self,
        title,
        dir,
        subtitle="",
        *,
        range_start=0,
        range_num=None,
        duration=60,
        amount=None,
    ):
        super().__init__(
            title + " " + subtitle,
            range_start=range_start,
            range_num=range_num,
            duration=duration,
            amount=amount,
        )
        self._dir: str = dir
        self._filename: str = title

    def _load_lines(self) -> list[str]:
        with open(f"dicts/{self._dir}/{self._filename}") as f:
            return f.readlines()
