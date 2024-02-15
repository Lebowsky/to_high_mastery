import sys
import asyncio
from asyncio.trsock import TransportSocket
import functools
from typing import cast

from charindex import InvertedIndex

CRLF = b'\r\n'
PROMPT = b'?> '


async def finder(index: InvertedIndex,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    client = writer.get_extra_info('peername')
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'

        print(f' From {client}: {query!r}')
        if query:
            if ord(query[:1]) < 32:
                break
            results = await search(query, index, writer)
            print(f'   To {client}: {results} results')

    writer.close()
    await writer.wait_closed()
    print(f'Close {client}.')


async def search(query: str,
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    pass


async def supervisor(index: InvertedIndex, host: str, port: int):
    server = await asyncio.start_server(functools.partial(finder, index), host, port)

    socket_list = cast(tuple[TransportSocket, ...], server.sockets)
    addr = socket_list[0].getsockname()
    print(f'Serving on {addr}. Hit Ctrl+C to stop.')
    await server.serve_forever()


def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Build index...')
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index, host, port))
    except KeyboardInterrupt:
        print('\nServer shut down.')


if __name__ == '__main__':
    main(*sys.argv[1:])
