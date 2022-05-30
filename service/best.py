import json
import re
import time

import requests
from conf import conf
import parser_html
import save_mysql


class BaseCategory:
    def __init__(self, country):
        self.country = country
        self.base_url = conf.country2url[self.country]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        self.session = requests.Session()

    def request_base(self):
        res = self.session.get(self.base_url, headers=self.headers)
        print(res)


class BestSeller:
    def __init__(self, country: str):
        self.country = country
        self.session = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }

        self.thirty_html_filed = {}
        self.thirty_html_list = []
        self.falls_html_list = []

    # def get_level1_category(self):
    #     parser_html.ParseCategory().parse_level1(self.cookie_tree.first_html)

    # 直接请求的前30个商品的页面信息
    def request_thirty_html_list(self, page=2):
        for i in [k+1 for k in range(page)]:
            url = 'https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices?&pg={}'.format(
                i)
            headers = self.headers
            # headers['cookie'] = self.cookie_str
            res = self.session.get(url=url, headers=headers)
            self.thirty_html_list.append(res.text)

    def parse_thirty_html_filed(self):
        self.thirty_html_filed['data_acp_params_list'] = []
        self.thirty_html_filed['script_list_list'] = []
        self.thirty_html_filed['acp_path_list'] = []
        for thirty_html in self.thirty_html_list:
            data_acp_params = re.findall('data-acp-params="(.*?)"', thirty_html)[0]
            self.thirty_html_filed['data_acp_params_list'].append(data_acp_params)

            script_list_string = re.match(r"[\s\S]*?data-client-recs-list=\"([\s\S]*?)\" data-index-offset", thirty_html).group(1).replace("&quot", '"').replace(";", "")
            script_list = json.loads(script_list_string)
            self.thirty_html_filed['script_list_list'].append(script_list)

            acp_path = re.findall('data-acp-path="(.*?)"', thirty_html)[0]
            self.thirty_html_filed['acp_path_list'].append(acp_path)

    def get_falls_xhr_post_prams(self):
        xhr_post_prams_list = []
        # 最外层是两页的filed信息
        for script_list in self.thirty_html_filed['script_list_list']:
            ids_list = []
            index_list = []
            for asin_info in script_list:
                if 30 <= script_list.index(asin_info) <= 50 or 80 <= script_list.index(asin_info) <= 100:
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
            xhr_post_prams_list.append(xhr_post_prams)
        return xhr_post_prams_list

    def request_falls_html_list(self):
        xhr_post_prams_list = self.get_falls_xhr_post_prams()
        for i in range(len(xhr_post_prams_list)):
            tok = re.findall('tok=(.*?);', self.thirty_html_filed['data_acp_params_list'][i])[0]
            rid = re.findall('rid=(.*?);', self.thirty_html_filed['data_acp_params_list'][i])[0]
            d1 = re.findall('d1=(.*?);', self.thirty_html_filed['data_acp_params_list'][i])[0]

            url = 'https://www.amazon.com{}nextPage?'.format(self.thirty_html_filed['acp_path_list'][i])
            time_stamp = int(time.time() + 152)
            headers_params = {
                "x-amz-acp-params": "tok={};ts={};rid={};d1={};d2=0".format(tok, time_stamp, rid, d1)
            }

            res = requests.post(url=url, headers=headers_params, data=json.dumps(xhr_post_prams_list[i]))
            self.falls_html_list.append(res.text)

    def request_one_category(self):
        self.request_thirty_html_list()
        self.parse_thirty_html_filed()
        self.get_falls_xhr_post_prams()
        self.request_falls_html_list()

        # parser_html.ParseProduct(self.thirty_html_list, self.falls_html_list).parse_product()
        item_list = parser_html.ParseCategory(self.country, self.thirty_html_list, 1).parse_category()
        for item in item_list:
            save_mysql.DBMysql().save_category(item)


def main():
    b = BestSeller('US')
    b.request_one_category()


if __name__ == '__main__':
    main()
