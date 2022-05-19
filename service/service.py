import re
import time

import requests
from conf import conf
from model import response


class BestSeller:


    def request_category(self):
        url = 'https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices'
        headers = self.headers
        headers['cookie'] = 'session-id={}; ubid-main={}; session-token={}'.format(self.session_id, self.ubid_main, self.session_token)
        res = self.session.get(url=url, headers=headers)
        print(res)
        print(res.text)


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


def test2():
    # 1652883607143
    # 1652962658936
    # 1652962580.2329466
    t = int(time.time()*1000)
    print(t)


def main():
    best = BestSeller("US")
    best.request_session_id()
    best.get_navigation_params()
    best.request_ubid_main()
    best.request_token()
    best.request_category()


if __name__ == '__main__':
    main()



