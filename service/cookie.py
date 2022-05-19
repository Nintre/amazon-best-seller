import re
import time

import requests
from conf import conf
from model import response


class CookieTree:
    def __init__(self, country):
        self.country = country
        self.bestsellers_url = conf.country2url[self.country]
        self.session = requests.Session()
        self.headers = {
            # "host": conf.country2host[self.country],
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        self.first_res = None
        self.session_id = None
        self.first_set_cookie = None
        self.ubid_main = None
        self.session_token = None

    # 拿到session_id和后面请求要用的cookie
    def request_session_id(self):
        self.first_res = self.session.get(self.bestsellers_url, headers=self.headers)
        self.first_set_cookie = self.first_res.headers['set-cookie']
        self.session_id = re.findall('session-id=(.*?);', self.first_set_cookie)[0]

    def request_ubid_main(self):
        time_stamp = int(time.time()*1000)
        url = 'https://www.amazon.com/portal-migration/hz/glow/get-rendered-toaster?pageType=zeitgeist&aisTransitionState=in&rancorLocationSource=REALM_DEFAULT&_={}'.format(time_stamp)
        headers = self.headers
        headers["cookie"] = self.first_set_cookie
        res = self.session.get(url=url, headers=headers)
        self.ubid_main = re.findall('ubid-main=(.*?);', res.headers['set-cookie'])[0]
        print(self.ubid_main)

    def get_navigation_params(self):
        res_text = self.first_res.text
        hash_customer_and_session_id = re.findall("hashCustomerAndSessionId','(.*?)'", res_text)[0]
        navigation_params = {
            'ajaxTemplate': 'hMenuDesktopFirstLayer',
            'pageType': 'zeitgeist',
            'hmDataAjaxHint': 1,
            'isFreshRegion': 'false',
            'isFreshCustomer': 'false',
            'isPrimeMember': 'false',
            'isPrimeDay': 'false',
            'isSmile': 'false',
            'isBackup': 'false',
            'firstName': 'false',
            'navDeviceType': 'desktop',
            'hashCustomerAndSessionId': hash_customer_and_session_id,
            'isExportMode': 'true',
            'environmentVFI': 'AmazonNavigationCards/development@B6080359880-AL2_x86_64',
            'languageCode': conf.language_code[self.country]
        }
        return navigation_params

    def request_token(self):
        params = self.get_navigation_params()
        header = self.headers
        header["cookie"] = 'session-id={}; i18n-prefs=USD; lc-main=en_US; ubid-main={}'.format(self.session_id, self.ubid_main)
        url = 'https://www.amazon.com/gp/navigation/ajax/generic.html?'
        res = self.session.get(url=url, headers=header, params=params)

        self.session_token = re.findall('session-token=(.*?);', res.headers['set-cookie'])[0]

    def get_cookie_str(self):
        self.request_session_id()
        self.get_navigation_params()
        self.request_ubid_main()
        self.request_token()
        return 'session-id={}; ubid-main={}; session-token={}'.format(self.session_id, self.ubid_main, self.session_token)
