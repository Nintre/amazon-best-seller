from lxml import etree


class ParseHtml:
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
    def __init__(self):
        pass

    def parse_level1(self, html):
        tree = etree.HTML(html)
        top_cate_name_elements = tree.xpath(".//div[@role='group']//div[@role='treeitem']")
        for top_cate in top_cate_name_elements:
            top_cate_url = top_cate.xpath("./a/@href")[0]
            top_cate_name = top_cate.xpath('./a/text()')[0]
            print(top_cate_name, top_cate_url)
