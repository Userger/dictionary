from modules.util import create_stdin_reader
import asyncio
import tty
import sys

async def main():
    tty.setcbreak(sys.stdin)
    reader = await create_stdin_reader()
    while (s := await reader.read(4)) != b'\n':
        print(s)

if __name__ == '__main__':
    asyncio.run(main())
