import json
import re
import time

import requests
import cookie
import parser_html


class BestSeller:
    def __init__(self, country: str):
        self.country = country
        self.session = requests.Session()
        self.headers = {
            # "host": conf.country2host[self.country],
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        self.cookie_tree = cookie.CookieTree(country)
        self.cookie_str = self.cookie_tree.get_cookie_str()
        self.acp_params = None
        self.acp_path = None
        self.script_list = None

        self.ahead_res = []
        self.more_res = []

    def get_level1_category(self):
        parser_html.ParseCategory().parse_level1(self.cookie_tree.first_html)

    # 这一步只能拿到第一页的前30个商品
    def request_ahead(self, page):
        url = 'https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices?&pg={}'.format(page)
        headers = self.headers
        headers['cookie'] = self.cookie_str
        res = self.session.get(url=url, headers=headers)
        self.ahead_res.append(res.text)
        self.acp_params = re.findall('data-acp-params="(.*?)"', res.text)[0]

        script_list_string = re.match(r"[\s\S]*?data-client-recs-list=\"([\s\S]*?)\" data-index-offset",
                                      res.text).group(1).replace("&quot", '"').replace(";", "")
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
        self.more_res.append(res.text)

    def request_one_category(self):
        for i in [1, 2]:
            self.request_ahead(i)
            self.request_falls()

        parser_html.ParseHtml(self.ahead_res, self.more_res).parse_product()


def main():
    b = BestSeller('US')
    b.get_level1_category()
    b.request_one_category()


if __name__ == '__main__':
    main()
