from function_scheduling_distributed_framework import task_deco
import re
import requests
from parsel import Selector
from pathlib import Path

"""
http://www.5442tu.com/mingxing/list_2_1.html  下载所有明星图片
"""


@task_deco('xiaoxianrou_list_page', qps=0.05)
def cralw_list_page(page_index):
    url = f'http://www.5442tu.com/mingxing/list_2_{page_index}.html'
    resp = requests.get(url)
    sel = Selector(resp.content.decode('gbk'))
    detail_sels = sel.xpath('//div[@class="imgList2"]/ul/li/a[1]')
    for detail_sel in detail_sels:
        crawl_detail_page.push(detail_sel.xpath('./@href').extract_first(), detail_sel.xpath('./@title').extract_first(), 1, is_first_picture=True)


@task_deco('xiaoxianrou_detail_page', qps=2,do_task_filtering=True)
def crawl_detail_page(url, title, picture_index, is_first_picture=False,):
    resp = requests.get(url)
    sel = Selector(resp.content.decode('gbk'))
    if is_first_picture:  # 详情页图册也需要翻页。
        total_page_str = sel.xpath('//div[@class="page"]/ul/li/a/text()').extract_first()
        total_page = int(re.search(r'共(\d+)页', total_page_str).group(1))
        for p in range(2, total_page + 1):
            next_pic_page_url = url[:-5] + f'_{p}.html'
            crawl_detail_page.push(next_pic_page_url, title, picture_index=p)
    pic_url = sel.xpath('//p[@align="center"]/a/img/@src').extract_first()
    resp_pic = requests.get(pic_url)
    Path(f'./pictures/{title}/').mkdir(parents=True, exist_ok=True)
    (Path(f'./pictures/{title}/') / Path(f'./{title}_{picture_index}.jpg')).write_bytes(resp_pic.content)  # 保存图片。
    print(f'''保存图片成功：\n {(Path(f'./pictures/{title}/') / Path(f'./{title}_{picture_index}.jpg')).absolute()} ''')


if __name__ == '__main__':
    # cralw_list_page(1)
    # crawl_detail_page('https://www.5442tu.com/mingxing/20181105/78924.html','范冰冰弟弟范丞丞阳光帅气明星壁纸图片高清',1,True)
    cralw_list_page.clear()
    crawl_detail_page.clear()

    for p in range(1, 10):
        cralw_list_page.push(p)

    cralw_list_page.consume()
    crawl_detail_page.consume()
