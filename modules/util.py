import sys
import asyncio
from asyncio import StreamReader, StreamWriter
async def create_stdin_reader():
    reader = StreamReader()
    def factory_protocol():
        return asyncio.StreamReaderProtocol(reader)
    pool = asyncio.get_running_loop()
    await pool.connect_read_pipe(factory_protocol, sys.stdin)
    return reader



