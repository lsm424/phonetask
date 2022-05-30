from threading import Thread
from comm.log import logger
import socketio
import time


def create_client():
    sio = socketio.Client()
    @sio.event
    def connect():
        logger.info('connection established')
        sio.emit('client', {'foo': 'bar'})

    @sio.on('serve')
    def on_message(data):
        print('client received a message!',data)

    @sio.on('last')
    def on_last(data):
        print('last ', data)
    # @sio.event
    # def message(data):
    #     print('message received with ', data)
    #     sio.emit('client', {'response': 'my response'})

    @sio.event
    def connect_error():
        print("The connection failed!")
        sio.disconnect()

    @sio.event
    def disconnect():
        print('disconnected from server')
        sio.disconnect()

    sio.connect('http://localhost:5000')
    sio.wait()



class LoginSocket():
    def __init__(self, url, namespace):
        self.sio = socketio.Client()
        self.sio.on('connect', self.connect, namespace='/xxxx')
        self.sio.connect(url, namespaces='/xxxx', wait=True, wait_timeout=3)
        self.sio.on('connect_error', self.connect_error)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('lai', self.on_lai, namespace='/xxxx')
        self.sio.on('last', self.on_last, namespace='/xxxx')

    def connect(self):
        print('connection established')

    def emit(self):
        self.sio.emit('client', {'foo': 'bar'}, namespace='/xxxx')

    def on_lai(self, data):
        print('client received a message!', data)
        self.sio.emit('last', {'foo': '111'}, namespace='/xxxx')

    def on_last(self, data):
        print('last ', data)

    # @sio.event
    # def message(data):
    #     print('message received with ', data)
    #     sio.emit('client', {'response': 'my response'})

    def connect_error(self, data):
        print("The connection failed!")
        self.sio.disconnect()

    def disconnect(self):
        print('disconnected from server')
        self.sio.disconnect()


class WebSocketClientBase(Thread):

    def __init__(self, app_name, url, login_code):
        Thread.__init__(self)
        self.app_name = app_name
        self.login_code = login_code
        self.url = url
        self.logined = False
        self.sio = socketio.Client()
        self.sio.on('connect', self.connect)
        self.sio.on('connect_error', self.connect_error)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('logined', self.on_logined)
        self.sio.on('ping', self.on_ping)

    def on_ping(self, data):
        logger.info(f'收到 ping， {data}')

    def connect(self):
        logger.info(f'{self.app_name} 建立webscoket连接')
        self.sio.emit('login', {'code': self.login_code})

    def connect_error(self, data):
        logger.warning(f"{self.app_name} 连接失败 {data}")
        self.sio.disconnect()
        self.logined = False

    def disconnect(self):
        logger.warning(f'{self.app_name} 和服务器断开连接')
        self.sio.disconnect()
        self.logined = False

    def on_logined(self, data):
        if data.get('status', False) is True:
            self.logined = True
            logger.info(f'{self.app_name} 登录成功')
        else:
            logger.info(f'{self.app_name} 登录失败 {data}')
            self.logined = False

    def run(self):
        while True:
            if self.logined:
                time.sleep(1)
                continue

            try:
                self.sio.connect(self.url)
            except BaseException as e:
                logger.error(f'发起连接失败 {e}')
            time.sleep(5)


if __name__ == '__main__':
    w = LoginSocket('http://127.0.0.1:5000', '/xxxx')
    time.sleep(1)
    w.emit()
    while True:
        import time
        time.sleep(10)
# create_client()

