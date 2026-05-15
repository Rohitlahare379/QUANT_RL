import asyncio
import websockets
import json

async def test():
    try:
        async with websockets.connect('ws://localhost:8000/ws/simulate') as websocket:
            await websocket.send(json.dumps({
                "code": "from simulator.interfaces.strategy import Strategy\nfrom simulator.signals.enums import Signal\nclass TestStrategy(Strategy):\n    def on_candle(self, candle, history):\n        return Signal.BUY",
                "symbol": "BTCUSDT",
                "speed_multiplier": 1000.0
            }))
            for _ in range(5):
                response = await websocket.recv()
                print(response)
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
