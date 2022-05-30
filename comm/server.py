import eventlet
import socketio
from flask import Flask


def create_serve():
    sio = socketio.Server(async_mode='threading')
    # app = socketio.WSGIApp(sio, static_files={
    #     '/': {'content_type': 'text/html', 'filename': 'index.html'}
    # })
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    @sio.on('last')
    def last(sid, data):
        print(f'last {data}')

    # @sio.on('client')
    # def on_message(sid, data):
    #     print('serve received a message!111', data)
    @sio.on('client')
    def another_event(sid, data):
        print('serve received a message!', data)
    # @sio.event
    # def my_event(sid, data):
    #     print('message ', data)
    #     sio.emit('serve', {'response': 'connert success'})
    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    def run():
        app.run('0.0.0.0', 5000)
        # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

    if __name__ == '__main__':
        import threading
        t = threading.Thread(target=run)
        t.setDaemon(True)
        t.start()

        # self.sio = socketio.Server(async_mode='eventlet', ping_timeout=60)
        # self.app = socketio.WSGIApp(self.sio)

        sio.emit('serve', {'response': 'connert success'})
        t.join()


create_serve()
