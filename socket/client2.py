#!/usr/bin/python3
import socket
import time
 
def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as streamSocket:
        # RaspberryPiへ10000番ポートで接続
        # ラズパイはデフォルトでraspberrypi.localというPC名が設定されています
        streamSocket.connect(('169.254.227.158', 10000))
        # サーバーからのメッセージ受信待ち
        byteData = streamSocket.recv(1024)
        print(byteData)
        # サーバーからのメッセージ受信待ち
        byteData = streamSocket.recv(1024)
        print(byteData)
        time.sleep(1)
        # サーバーへメッセージ送信
        streamSocket.sendall(b'from client 1st message')
        time.sleep(1)
        # サーバーへメッセージ送信
        streamSocket.sendall(b'from client 2st message')
 
if __name__ == "__main__":
    start()