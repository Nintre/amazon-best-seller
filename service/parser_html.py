import datetime

from lxml import etree


class ParseProduct:
    def __init__(self, ahead_res_list, more_res_list):
        self.ahead_res_list = ahead_res_list
        self.more_res_list = more_res_list

    def parse_product(self):
        for res in self.ahead_res_list:
            tree = etree.HTML(res)
            url = tree.xpath('//a[@class="a-link-normal"]/@href')[0]
            rank = tree.xpath('//span[@class="zg-bdg-text"]/text()')
            print(rank)

        for res in self.more_res_list:
            tree = etree.HTML(res)
            url = tree.xpath('//a[@class="a-link-normal"]/@href')[0]
            rank = tree.xpath('//span[@class="zg-bdg-text"]/text()')
            print(rank)


class ParseCategory:
    def __init__(self, country, ahead_res_list, level):
        self.country = country
        self.ahead_html = ahead_res_list[0]
        self.level = level
        self.item_list = []

    def parse_category(self):
        tree = etree.HTML(self.ahead_html)
        cate_name_elements = tree.xpath(".//div[@role='group']//div[@role='treeitem']")
        for cate in cate_name_elements:
            item = {'country': self.country, 'level': self.level}
            cate_url = cate.xpath("./a/@href")[0]
            cate_name = cate.xpath('./a/text()')[0]
            item['url'] = cate_url
            item['category_name'] = cate_name
            item['snapshot_date'] = str(datetime.datetime.now()).split('.')[0]
            self.item_list.append(item)

        return self.item_list


