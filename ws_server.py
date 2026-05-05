import argparse
import asyncio
import json
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


async def handler(websocket):
    print('Client connected.')

    await websocket.send(json.dumps({'message': 'Hello from server!'}))

    try:
        async for message in websocket:
            print('Received from client:', message)

            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                data = {'raw': message}

            await websocket.send(json.dumps({
                'type': 'echo',
                'received': data
            }))

    except ConnectionClosedOK:
        print('Client disconnected gracefully.')
    except ConnectionClosedError as e:
        print('Client disconnected with error:', e)


async def main(port: int):
    async with websockets.serve(handler, '0.0.0.0', port):
        print(f'WebSocket server running on ws://localhost:{port}')
        try:
            await asyncio.Future()  # wait forever
        except asyncio.CancelledError:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simple WebSocket echo server.'
    )
    parser.add_argument(
        'port',
        nargs='?',
        type=int,
        default=8080,
        help='Port to listen on (default: 8080)'
    )

    args = parser.parse_args()

    try:
        asyncio.run(main(args.port))
    except KeyboardInterrupt:
        print('\nServer stopped by user.')