#encoding=utf-8
import time

from comm.common import system, MAC, PHONE, restart_fly_mode, restart_wifi
from comm.log import logger
from comm.ua import ua
from heli.api.heli import Heli
from websocket_manager.websocket_client import WebSocketClientBase


# 预约动作
def perservation(phone, shopid, token):
    h = Heli()
    user_agent = ua.get_ua()
    r = h.get_acts12_dateinfo(token, user_agent)
    r = h.get_default_config(token, user_agent)
    r = h.save_s12_sign(token, shopid, user_agent)
    if r == '7天内只能报名一次':
        return {'code': 0, 'message': r, 'token': token}
    elif r == '报名成功':
        r = h.get_s12_member_sign(token)
        if r.get('shopCode', '') == shopid and r.get('memberId', '') == phone:
            return {'code': 0, 'message': '报名成功', 'token': token, 'ipAddr': r['ipAddr']}
        return {'code': -2, 'message': f'报名成功但是未查询到结果: {r}', 'token': token, 'ipAddr': r.get('ipAddr', '')}
    return {'code': -1, 'message': r, 'token': token}


class HeliWebSocketClient(WebSocketClientBase):
    def __init__(self, app_name, url, login_code):
        WebSocketClientBase.__init__(self, app_name, url, login_code)
        self.sio.on('perservation', self.on_perservation)

    # 执行预约
    # 请求：{'reboot_fly': True/False, 'data': {'phone': phone, 'shop_code':
    # shop_code, 'token': token, 'perservation_id': data['id']}}
    # 返回 {'phone': 'xxx', 'code': x, 'msg': '', 'token': 'xxx', 'ipAddr': 'xxx', 'perservation_id': 'xx'}
    def on_perservation(self, data):
        logger.info(f'收到预约请求: {data}')
        args = data['data']
        r = perservation(phone=args['phone'], shopid=args['shop_code'], token=args['token'])
        r['token'] = r['token']
        r['phone'] = args['phone']

        logger.info(f'响应：{r}')
        self.sio.emit('perservation_result', r)
        time.sleep(1)
        if data.get('reboot_fly', False) is True:
            p = system()
            if p == MAC:
                self.disconnect()
            elif p == PHONE:
                restart_fly_mode()
                restart_wifi()


if __name__ == '__main__':
    from comm.log import gen_log
    gen_log('heli_client')

    w = HeliWebSocketClient('合力', 'http://127.0.0.1:5000', 'heli')
    w.start()
    w.join()
