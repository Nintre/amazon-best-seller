import re

import requests
from conf import conf
from model import response


class BestSeller:
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
        self.session_id_token = None
        self.ubid_main = None
        self.session_token = None

    def get_session_id_token(self):
        self.first_res = self.session.get(self.bestsellers_url, headers=self.headers)
        self.session_id_token = self.first_res.headers['set-cookie']
        self.session_id = re.findall('session-id=(.*?);', self.session_id_token)[0]

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

    def get_ubid_main(self):
        url = 'https://www.amazon.com/portal-migration/hz/glow/get-rendered-toaster?pageType=zeitgeist&aisTransitionState=in&rancorLocationSource=REALM_DEFAULT&_=1652883607143'
        headers = self.headers
        headers["cookie"] = self.session_id_token
        res = self.session.get(url=url, headers=headers)
        self.ubid_main = re.findall('ubid-main=(.*?);', res.headers['set-cookie'])[0]
        print(self.ubid_main)

    def get_token(self):
        params = self.get_navigation_params()
        header = self.headers
        header["cookie"] = 'session-id={}; i18n-prefs=USD; lc-main=en_US; ubid-main={}'.format(self.session_id, self.ubid_main)
        url = 'https://www.amazon.com/gp/navigation/ajax/generic.html?'
        res = self.session.get(url=url, headers=header, params=params)

        self.session_token = re.findall('session-token=(.*?);', res.headers['set-cookie'])[0]
        print(self.session_token)



def test():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        'cookie': 'session-id=147-3762806-8750218; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:CN"; ubid-main=130-6275166-0398955; csm-hit=tb:Z4SJNQNKQA57F1B0TWM8+s-Z4SJNQNKQA57F1B0TWM8|1652882264460&t:1652882264460&adb:adblk_no'
    }
    a = 'https://www.amazon.com/gp/navigation/ajax/generic.html?ajaxTemplate=hMenuDesktopFirstLayer&pageType=zeitgeist&hmDataAjaxHint=1&isFreshRegion=false&isFreshCustomer=false&isPrimeMember=false&isPrimeDay=false&isSmile=false&isBackup=false&firstName=false&navDeviceType=desktop&hashCustomerAndSessionId=b023caf48fb5629ed2c66b4ab490b174a66cb23f&isExportMode=true&environmentVFI=AmazonNavigationCards%2Fdevelopment%40B6080359880-AL2_x86_64&languageCode=en_US'
    res = requests.get(url=a, headers=headers)
    print(res)
    print(res.cookies)
    print(res.headers)
    print(res.headers['set-cookie'])


if __name__ == '__main__':
    best = BestSeller("US")
    best.get_session_id_token()
    best.get_navigation_params()
    best.get_ubid_main()
    best.get_token()
    # test()



