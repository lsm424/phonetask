#encoding=utf-8

from comm.common import system, PHONE, MAC
from comm.log import gen_log
from heli.websocket.client import HeliWebSocketClient

if __name__ == '__main__':
    gen_log('phone')

    host = '127.0.0.1'
    if system() in (PHONE, MAC):
        host = '140.246.143.7'
    w = HeliWebSocketClient('合力', f'http://{host}:5000', 'heli')
    w.setDaemon(True)
    w.start()
    w.join()

