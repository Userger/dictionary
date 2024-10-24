import os
import sys
import asyncio
import random
import time
from .util import create_stdin_reader
from .exceptions import Escape

class GameProcess:
    def __init__(self, reader, *,
                 duration,
                 dictionary):
        self._duration = duration
        self._dict = dictionary
        self._reader = reader
        self.fails = 0
        self.points = 0

    async def start(self):
        self._draw_msg = Drawer(1, 1).draw
        self._draw_msg2 = Drawer(1, 2).draw
        self._draw_time = Drawer(1, 3).draw
        self._draw_word = Drawer(1, 4).draw
        self._read_word = InputReader(1, 6, self._reader).read
        self._draw_translates = Drawer(1, 9).draw

        tasks = [t_task := asyncio.create_task(self._timer()),
                 p_task := asyncio.create_task(self._process())]
        done, pending = await asyncio.wait(tasks,
                           return_when=asyncio.FIRST_COMPLETED)
        [task.cancel() for task in pending]
        await asyncio.sleep(0)
        return {'points': self.points,
                'fails': self.fails,
                'exited': done.pop().result()}


    async def _timer(self):
        start = int(time.time()) + self._duration
        count = self._duration
        while count > 0:
            self._draw_time(f'Time: {count}')
            await asyncio.sleep(1)
            count = start - int(time.time())
        return 'timeout'


    async def _check(self, en_word, translates):
        old_fails = self.fails

        while (await self._read_word()) not in translates:
            self.fails += 1
            self._draw_translates(f'possible translates: {translates}')
            self._draw_msg('Fails++')
            self._draw_msg2(f'points: {self.points} / fails: {self.fails}')

        if old_fails == self.fails:
            self.points += 1


    async def _process(self):
        os.system('clear')
        order = list(range(len(self._dict)))
        self._draw_msg2(f'points: {self.points} / fails: {self.fails}')
        try:
            while True:
                random.shuffle(order)
                for i in order:
                    word, translates = self._dict[i]
                    self._draw_word(word)
                    await self._check(word, translates)
                    self._draw_msg('Point++')
                    self._draw_msg2(f'points: {self.points} / '
                                    f'fails: {self.fails}')
                    self._draw_translates(f'previous translates: {translates}')
        except Escape:
            return 'escape'


class Drawer:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def draw(self, string):
        sys.stdout.write('\0337')
        sys.stdout.write(f'\033[{self._y};{self._x}H')
        sys.stdout.write('\033[K')
        sys.stdout.write(string)
        sys.stdout.write('\0338')
        sys.stdout.flush()


class InputReader:
    def __init__(self, x, y, reader):
        self._x = x
        self._y = y
        self._reader = reader

    async def read(self):
        sys.stdout.write(f'\033[{self._y};{self._x}H')
        sys.stdout.write('\033[K')
        sys.stdout.flush()
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


        return ''.join(chars).strip()


