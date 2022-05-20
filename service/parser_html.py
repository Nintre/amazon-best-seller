from lxml import etree


class ParseHtml:
    def __init__(self, ahead_res_list, more_res_list):
        self.ahead_res_list = ahead_res_list
        self.more_res_list = more_res_list

    def parse_product(self):
        for res in self.ahead_res_list:
            tree = etree.HTML(res)
            url = tree.xpath('//a[@class="a-link-normal"]/@href')[0]
            rank = tree.xpath('//span[@class="zg-bdg-text"]/text()')[0]
            print(rank)

        for res in self.more_res_list:
            tree = etree.HTML(res)
            url = tree.xpath('//a[@class="a-link-normal"]/@href')[0]
            rank = tree.xpath('//span[@class="zg-bdg-text"]/text()')[0]
            print(rank)


def get_product(ahead_res_list, more_res_list):
    ParseHtml(ahead_res_list, more_res_list).parse_product()

