import asyncio
import websockets

async def listen_websocket():
    url = "ws://192.168.18.32:8000/api/ws"  # Replace "your_server_address" with the actual WebSocket server address

    try:
        async with websockets.connect(url) as websocket:
            print("Connected to WebSocket server.")
            while True:
                data = await websocket.recv()
                print(f"Received data: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_websocket())