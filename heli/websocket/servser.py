#encoding=utf-8
import datetime
from comm.log import logger
from heli.dao.account import account_table, THeliAccountInfo
from heli.comm.comm import update_status
from websocket_manager.websocket_server import WebSocketBaseServer, websocket_server


class WebSocketHeli(WebSocketBaseServer):
    def __init__(self, app_name, login_code, max_task_cnt):
        WebSocketBaseServer.__init__(self, app_name, max_task_cnt)
        self.login_code = login_code

    # 登录码
    def get_login_code(self) -> str:
        return self.login_code

    # 回传预约结果  {'phone': 'xxx', 'code': x, 'msg': '', 'token': 'xxx', 'ipAddr': 'xxx', 'perservation_id': 'xx'}
    def on_perservation_result(self, sid, data):
        phone = data.get('phone', '')
        if not phone:
            logger.warning(f'【websocketserver】{self.app_name} 预约结果没有带手机号，resp: {data}')
            return

        r = data
        token = data['token']

        if r['code']:
            logger.error(f'{phone}预约失败，{r}')
            account_table.update_account(phone, THeliAccountInfo.ACCOUNT_PERSERVATION_FAILD, r['message'], token=token)
        else:
            logger.error(f'{phone}预约成功！！！，{r}')
            account_table.update_account(phone, THeliAccountInfo.ACCOUNT_PERSERVATIONED, r['message'], token=token)
            update_status(phone)
        # account_table.update_account(phone, account_status, r['message'],
        #                              perservation_time=now, ip=r.get('ipAddr', ''))


# 注册heli websocket
websocket_heli_server = WebSocketHeli("合力", 'heli', 1)
websocket_server.register_app(websocket_heli_server)

if __name__ == '__main__':
    import time
    from comm.log import gen_log
    gen_log('heli_server')

    websocket_server.start()

    while True:
        # websocket_server.push_task('合力', 'ping', {'ping': True})
        time.sleep(5)