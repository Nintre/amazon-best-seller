import json
import re
import time

import requests
from conf import conf
from model import response
import cookie


class BestSeller:
    def __init__(self, country: str):
        self.country = country
        self.session = requests.Session()
        self.headers = {
            # "host": conf.country2host[self.country],
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        self.cookie_tree = cookie.CookieTree(country).get_cookie_str()

        self.acp_params = None
        self.acp_path = None
        self.script_list = None

    # 这一步只能拿到第一页的前30个商品
    def request_category(self):
        url = 'https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices'
        headers = self.headers
        headers['cookie'] = self.cookie_tree
        res = self.session.get(url=url, headers=headers)
        self.acp_params = re.findall('data-acp-params="(.*?)"', res.text)[0]
        print(self.acp_params)

        script_list_string = re.match(r"[\s\S]*?data-client-recs-list=\"([\s\S]*?)\" data-index-offset", res.text).group(1).replace("&quot", '"').replace(";", "")
        self.script_list = json.loads(script_list_string)
        self.acp_path = re.findall('data-acp-path="(.*?)"', res.text)[0]

    def get_falls_params(self):
        ids_list = []
        index_list = []
        for asin_info in self.script_list:
            if 30 <= self.script_list.index(asin_info) <= 50 or 80 <= self.script_list.index(asin_info) <= 100:
                rank = asin_info['metadataMap']['render.zg.rank']
                asin = asin_info["id"]
                ids_string = "{\"id\":\"%s\",\"metadataMap\":{\"render.zg.rank\":\"%s\",\"render.zg.bsms.currentSalesRank\":\"\",\"render.zg.bsms.percentageChange\":\"\",\"render.zg.bsms.twentyFourHourOldSalesRank\":\"\"},\"linkParameters\":{}}" % (
                    asin, rank)
                ids_list.append(ids_string)
                index_list.append(int(rank))
        off_set = str(len(ids_list))
        xhr_post_prams = {
            "faceoutkataname": "GeneralFaceout",
            "ids": ids_list,
            "indexes": index_list,
            "linkparameters": "",
            "offset": off_set,
            "reftagprefix": "zg_bs_amazon-devices"
        }
        return xhr_post_prams

    def request_falls(self):
        xhr_post_prams = self.get_falls_params()
        tok = re.findall('tok=(.*?);', self.acp_params)[0]
        rid = re.findall('rid=(.*?);', self.acp_params)[0]
        d1 = re.findall('d1=(.*?);', self.acp_params)[0]

        url = 'https://www.amazon.com{}nextPage?'.format(self.acp_path)
        time_stamp = int(time.time() + 152)
        headers_params = {
            "x-amz-acp-params": "tok={};ts={};rid={};d1={};d2=0".format(tok, time_stamp, rid, d1)
        }

        res = requests.post(url=url, headers=headers_params, data=json.dumps(xhr_post_prams))
        print(res)
        print(res.json)
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


def main():
    b = BestSeller('US')
    b.request_category()
    b.request_falls()


if __name__ == '__main__':
    main()



