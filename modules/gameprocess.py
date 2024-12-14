import asyncio
import os
import random
import sys
import time
from dataclasses import dataclass

from .exceptions import Escape


class GameProcess:
    reader: asyncio.StreamReader
    dct: list[tuple[str, list[str]]]
    fails: int
    points: int
    order: list[int]
    fail_words: dict[str, list[str]]

    duration: None | int
    amount: None | int

    tasks: list[asyncio.Task[str]]
    done: set[asyncio.Task[str]]
    pend: set[asyncio.Task[str]]

    word: str
    translates: list[str]

    def __init__(self, reader, *, duration, dictionary, amount=None):
        self.duration = duration
        self.dct = dictionary
        self.amount = amount
        self.reader = reader
        self.fails = 0
        self.points = 0
        self.fail_words = {}
        self.order = list(range(len(self.dct)))
        self.init_drawers()

    def init_drawers(self):
        self.draw_msg = Drawer(1, 1).draw
        self.draw_msg2 = Drawer(1, 2).draw
        self.draw_time = Drawer(1, 3).draw
        self.draw_word = Drawer(1, 4).draw
        self.read_word = InputReader(1, 6, self.reader).read
        self.draw_translates = Drawer(1, 9).draw

    def init_tasks(self):
        process_task = asyncio.create_task(self.process())
        self.tasks = [process_task]
        if self.duration:
            timer_task = asyncio.create_task(self.timer())
            self.tasks.append(timer_task)

    async def run(self):
        self.init_tasks()
        await self.wait_first_complete_task()
        self.cancel_pending_tasks()
        await self.end_notify()

        return GameResult(
            points=self.points,
            fails=self.fails,
            exited=self.exited,
            failed_words=self.fail_words,
        )

    async def wait_first_complete_task(self):
        self.done, self.pend = await asyncio.wait(
            self.tasks, return_when=asyncio.FIRST_COMPLETED
        )

    def cancel_pending_tasks(self):
        [task.cancel() for task in self.pend]

    async def end_notify(self):
        os.system("clear")
        match exited := self.done.pop().result():
            case "timeout":
                print("TIME'S OUT")
            case "words out":
                print("Good Job!!!")
            case _:
                print("ESCAPED")
        await asyncio.sleep(0)
        await self.reader.read(4)
        self.exited = exited

    async def timer(self) -> str:
        if not self.duration:
            raise Escape()
        start = int(time.time()) + self.duration
        count = self.duration
        while count > 0:
            self.draw_time(f"Time: {count}")
            await asyncio.sleep(1)
            count = start - int(time.time())
        return "timeout"

    def on_success(self):
        if self.old_fails == self.fails:
            self.points += 1
            self.draw_msg("Points++")
            self.draw_translates(f'"{self.word}" translates: {self.translates}')
            self.draw_msg2(f"points: {self.points} / fails: {self.fails}")
            if self.is_game_over():
                raise WordsOut()

    def on_fail(self):
        self.fails += 1
        self.fail_words[self.word] = self.translates
        self.draw_translates(f"possible translates: {self.translates}")
        self.draw_msg("Fails++")
        self.draw_msg2(f"points: {self.points} / fails: {self.fails}")

    async def play_word_until_success(self, index):
        self.word, self.translates = self.dct[index]
        self.old_fails = self.fails
        self.draw_word(self.word)
        while await self.read_word() not in self.translates:
            self.on_fail()
        self.on_success()

    async def play_round(self):
        for i in self.order:
            await self.play_word_until_success(i)

    def reshufle_words_order(self):
        random.shuffle(self.order)

    async def process(self) -> str:
        os.system("clear")
        self.draw_msg2(f"points: {self.points} / fails: {self.fails}")
        try:
            while True:
                self.reshufle_words_order()
                await self.play_round()
        # when level with amount constraint (points == amount)
        except WordsOut:
            return "words out"
        # when user press 'esc'
        except Escape:
            return "escape"

    def is_game_over(self):
        return (self.points >= self.amount) if self.amount else False


class Drawer:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, string):
        sys.stdout.write("\0337")
        sys.stdout.write(f"\033[{self.y};{self.x}H")
        sys.stdout.write("\033[K")
        sys.stdout.write(string)
        sys.stdout.write("\0338")
        sys.stdout.flush()


class InputReader:
    def __init__(self, x, y, reader):
        self.x = x
        self.y = y
        self.reader = reader

    async def read(self):
        sys.stdout.write(f"\033[{self.y};{self.x}H")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        chars = []
        while (char := await self.reader.read(4)) != b"\n":
            if char == b"\x7F" and chars:
                chars.pop()
                sys.stdout.write("\033[D")
                sys.stdout.write(" ")
                sys.stdout.write("\033[D")
                sys.stdout.flush()
            elif char == b"\x1B":
                raise Escape()
            else:
                char = char.decode()
                chars.append(char)
                sys.stdout.write(char)
                sys.stdout.flush()

        return "".join(chars).strip()


@dataclass
class GameResult:
    points: int
    fails: int
    exited: str
    failed_words: dict[str, list[str]]


class WordsOut(Exception):
    pass
