import asyncio
# WebSocketモジュールを宣言する。
import websockets
 
# クライアント接続すると呼び出す。
async def accept(websocket, path):
  # 無限ループ
  while True:
    # クライアントからメッセージを待機する。
    data = await websocket.recv()
    # コンソールに出力
    print("receive : " + data)
    # クライアントでechoを付けて再送信する。
    await websocket.send("echo : " + data)
 
# WebSocketサーバー生成。ホストはlocalhost、portは9998に生成する。
start_server = websockets.serve(accept, "localhost", 9998)
# 非同期でサーバを待機する。
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()