#encoding=utf-8
from flask import Blueprint, request

from comm.log import logger
from websocket_manager.websocket_server import websocket_server

websocket_blue = Blueprint('websocket', __name__, url_prefix='/websocket')


@websocket_blue.route('/get_count', methods=['GET'])
def get_count():
    data = request.args.to_dict()
    logger.info(f'获取设备数量： {data}')
    app_name = str(data.get('app_name', '')).strip()
    return str(websocket_server.devices_count(app_name))