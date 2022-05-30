import json
import threading
import traceback

import eventlet
import socketio
import random

from flask import Flask

from comm.log import logger
from threading import RLock
from abc import ABCMeta, abstractmethod
import time


class WebSocketBaseServer(socketio.Namespace):
    __metaclass__ = ABCMeta                     #必须先声明

    def __init__(self, appname, max_task_cnt):
        socketio.Namespace.__init__(self)
        self.is_connect = False
        self.lock = RLock()
        self.app_name = appname
        self.connections = {}              # key：sid， value 次数
        self.max_task_cnt = max_task_cnt   # 一个连接最多只执行的任务次数

    # 收到连接回调
    def on_connect(self, sid, environ):
        logger.info(f'【websocketserver】{self.app_name} 收到连接 {sid} {environ}')

    # 断开连接回调
    def on_disconnect(self, sid):
        if sid in self.connections:
            self.connections.pop(sid)
            logger.warning(f'{self.app_name} sid {sid} 断开连接，总连接数:{len(self.connections)}')

    def on_connect_error(self, sid):
        if sid in self.connections:
            self.connections.pop(sid)
            logger.info(f'【websocket】 {self.app_name} 链路异常，总连接数:{len(self.connections)}')

    # 登录验证处理
    def on_login(self, sid, data):
        if data.get('code', '') != self.get_login_code():
            self.emit('logined', {'status': False}, room=sid, namespace=self.namespace)
            logger.warning(f'【websocketserver】{self.app_name} sid {sid} 登录失败， data: {data}')
            return

        self.emit('logined', {'status': True}, room=sid, namespace=self.namespace)
        with self.lock:
            self.connections[sid] = 0
        logger.warning(f'【websocketserver】{self.app_name} sid {sid} 登录成功， data: {data}，总连接数:{len(self.connections)}')

    # 发起任务 data格式：{'reboot_fly': True/False, 'data': task}
    def emit_task(self, cmd, task):
        try:
            with self.lock:
                while len(self.connections) > 0:
                    # 找一个使用次数最少的连接
                    sid = random.choice(list(self.connections))
                    self.connections[sid] += 1
                    data = {'data': task, 'reboot_fly': False}
                    if self.connections[sid] == self.max_task_cnt:      # 达到任务执行阈值时发起重启飞行模式
                        data['reboot_fly'] = True
                    elif self.connections[sid] > self.max_task_cnt:
                        continue
                    logger.info(f'【websocketserver】{self.app_name} 发送任务, cmd: {cmd}, sid {sid}, data: {data}')
                    self.emit(cmd, data, room=sid)
                    return {'code': 0}
                else:
                    return {'code': -1, 'msg': '无可用连接，稍后再试'}
        except BaseException as e:
            return {'code': -2, 'msg': f'发送任务异常: {e} {traceback.format_exc()}'}

    @abstractmethod
    def get_login_code(self) -> str:
        pass


class WebSocketServer:
    def __init__(self, port):
        self.sio = socketio.Server(async_mode='threading')
        self.app = Flask(__name__)
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
        self.port = port
        self.apps = {}
        # self.sio.on('connect', self.connect)
        # self.sio.on('disconnect', self.disconnect)
        # self.sio.on('client', self.another_event, namespace='/xxxx')

    def start(self):
        self.t = threading.Thread(target=self.run)
        self.t.setDaemon(True)
        self.t.start()

        # self.p = threading.Thread(target=self.ping)
        # self.p.setDaemon(True)
        # self.p.start()

    # 注册应用
    def register_app(self, app: WebSocketBaseServer):
        self.sio.register_namespace(app)
        self.apps[app.app_name] = app

    # 推送任务
    def push_task(self, app_name, cmd, task):
        if app_name not in self.apps:
            return {'code': -3, 'msg': f'{app_name} 未注册'}
        app = self.apps[app_name]
        return app.emit_task(cmd, task)

    # def connect(self, sid, env):
    #     print('connect ', sid, env)
    #     self.is_connected = True
    #     self.sio.emit('serve', {'asf': 10},  namespace='/xxxx')
    #
    # def disconnect(self, sid):
    #     print('disconnect ', sid)
    #     self.is_connected = False
    #
    # def another_event(self, sid, data):
    #     print('serve received a message!', data, sid)
    #     self.sio.emit('last', time.time(), namespace='/')

    def run(self):
        logger.info(f'--启动websocket, port: {self.port}')
        self.app.run('0.0.0.0', self.port)
        # eventlet.wsgi.server(eventlet.listen(('0.0.0.0', self.port)), self.app)

    def ping(self):
        while True:
            self.push_task('合力', 'ping', {'ping': True})
            time.sleep(5)

    # 设备数量
    def devices_count(self, app_name):
        if not app_name:
            return sum(map(lambda x: len(x.connections), self.apps.values()))
        if app_name not in self.apps:
            return 0
        return len(self.apps[app_name].connections)


websocket_server = WebSocketServer(5000)

if __name__ == '__main__':
    import time

    websocket_server.start()

    # 注册heli websocket
    from heli.websocket.servser import WebSocketHeli
    websocket_heli_server = WebSocketHeli("合力", 'heli', 1)
    websocket_server.register_app(websocket_heli_server)

    while True:
        websocket_server.push_task('合力', 'ping', {'ping': True})
        time.sleep(5)
