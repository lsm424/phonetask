#encoding=utf=8
import time

import requests
from comm.log import logger

# proxy = {
#     'http': 'http://106.32.10.70:4231',
#     'https': 'https://106.32.10.70:4231'
# }

proxy = None


class Heli:
    def __init__(self):
        self.s = requests.session()

    # 获取日期信息
    def get_acts12_dateinfo(self, token, user_agent):
        url = 'https://spec.helichaoshi.com/ActS12DateInfo'
        headers = {
            'Accept': 'application/json;charset=UTF-8;',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'JSESSIONID={token}',
            'User-Agent': user_agent,
            'Referer': 'https://servicewechat.com/wx06a6a21a08010030/84/page-frame.html',
            'Accept-Language': 'zh-cn',
        }
        try:
            r = self.s.get(url, headers=headers, verify=False, proxies=proxy)
            r.raise_for_status()
            r = r.json()
            return r
        except BaseException as e:
            logger.error(f'get acts12 datainfo 失败，{e}')
            return None

    # 获取日期信息
    def get_default_config(self, token, user_agent):
        url = 'https://spec.helichaoshi.com/getDefaultConfig.do'
        headers = {
            'Accept': 'application/json;charset=UTF-8;',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'JSESSIONID={token}',
            'User-Agent': user_agent,
            'Referer': 'https://servicewechat.com/wx06a6a21a08010030/84/page-frame.html',
            'Accept-Language': 'zh-cn',
        }
        try:
            r = self.s.post(url, headers=headers, verify=False, proxies=proxy)
            r.raise_for_status()
            if r.text == '':
                return {}
            r = r.json()
            return r
        except BaseException as e:
            logger.error(f'get defualt config 失败，{e}')
            return None

    # 预约
    def save_s12_sign(self, token, shop_id, user_agent):
        url = 'https://spec.helichaoshi.com/saveS12Sign'
        headers = {
            'Accept': 'application/json;charset=UTF-8;',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'JSESSIONID={token}',
            'User-Agent': user_agent,
            'Referer': 'https://servicewechat.com/wx06a6a21a08010030/84/page-frame.html',
            'Accept-Language': 'zh-cn',
        }
        try:
            r = self.s.post(url, headers=headers, verify=False, data=f'volumeType=1&shopCode={shop_id}', proxies=proxy)
            r.raise_for_status()
            r = r.text
            return r
        except BaseException as e:
            logger.error(f'save s12 sign 失败，{e}')
            return None

    # 查看预约结果
    def get_s12_member_sign(self, token):
        url = 'https://spec.helichaoshi.com/getS12MemberSign'
        headers = {
            'Accept': 'application/json;charset=UTF-8;',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'JSESSIONID={token}',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
            'Referer': 'https://servicewechat.com/wx06a6a21a08010030/84/page-frame.html',
            'Accept-Language': 'zh-cn',
        }
        try:
            r = self.s.post(url, headers=headers, verify=False, proxies=proxy)
            r.raise_for_status()
            if r.text == '':
                return {}
            r = r.json()
            return r
        except BaseException as e:
            logger.error(f'get s12 member sign 失败，{e}')
            return None