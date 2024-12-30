# -*- coding: utf-8 -*-
import requests
import time
from lxml import etree
import pandas as pd


#  作者:csdn.美味大香蕉
#  日期:2020-11-10

# 卍分割1.搜索的词与2.词在词库里的位置,※分割1.搜索的词与3.词的同义词

# 写入txt
def writeTxt(text):
    file = open('./data.txt', 'a', encoding='utf-8')
    file.write(text + "\n")
    file.close()


# 爬取网页
def Request(url):
    response = requests.get(url, timeout=10)
    time.sleep(2)
    # print(response)
    response.encoding = 'utf-8'
    textData = response.text
    resHtml = etree.HTML(textData.encode('utf-8'))
    return resHtml


# 主程序
def crawl():
    # 官网
    baseUrl = "https://www.ncbi.nlm.nih.gov"
    # 起始词All MeSH Categories
    queueHref = ["/mesh/1000048"]
    endHref = []
    # 统计写入txt的数据量
    num = 0
    # 标记错误链接的重试次数
    tag = 0
    # 开始时间
    startTime = time.time()
    while queueHref != []:
        try:
            headHref = queueHref[0]
            print(headHref)
            # 拼接url
            url = baseUrl + headHref
            # 获取网页
            html = Request(url)
            # 从网页上获取href
            xpath = '//*[@id="maincontent"]/div/div[5]/div//@href'
            hrefData = html.xpath(xpath)
            if len(hrefData) > 0:
                for h in hrefData:
                    if h not in endHref and h not in queueHref and h[:6] == "/mesh/":
                        queueHref.append(h)
            # 从网页上获取 词
            nameXpath = '//*[@id="maincontent"]/div/div[5]/div/h1/text()'
            nameData = html.xpath(nameXpath)
            # 从网页上获取 entryTerms
            entryTermsXpath = '//*[@id="maincontent"]/div/div[5]/div/ul[1]/*/text()'
            entryTermsData = html.xpath(entryTermsXpath)
            entryTerms = ""
            if len(entryTermsData) > 1:
                entryTermsData3 = []
                for e in range(len(entryTermsData)):
                    entryTermsXpath2 = '//*[@id="maincontent"]/div/div[5]/div/ul[1]/li[' + str(e + 1) + ']//text()'
                    entryTermsData2 = html.xpath(entryTermsXpath2)
                    if len(entryTermsData2) > 0:
                        entryTermsData3.append("".join(entryTermsData2))
                entryTerms = "※".join(entryTermsData3)
            elif len(entryTermsData) == 1:
                if entryTermsData[0] != "All MeSH Categories":
                    entryTerms = entryTermsData[0]
            # 从网页上获取 Tree Number(s)
            idXpath = '//*[@id="maincontent"]/div/div[5]/div/p/text()'
            idData = html.xpath(idXpath)
            if len(idData) > 0:
                for i2 in idData:
                    if "Tree Number(s): " in i2:
                        ids = i2.replace("Tree Number(s): ", "")
                        ids = ids.split(", ")
                        # 将数据写入txt
                        for id in ids:
                            writeTxt(id + "卍" + nameData[0] + "※" + entryTerms)
                            num += 1
                            print("已写入第" + str(num) + "个数据。")
            # 更新queueHref和endHref
            queueHref.remove(headHref)
            endHref.append(headHref)
            tag = 0
        except:
            # 若重试次数等于10次，就将错误的Href保存至errorLog.txt
            if tag == 10:
                queueHref.remove(headHref)
                endHref.append(headHref)
                file = open('./errorLog.txt', 'a', encoding='utf-8')
                file.write(headHref + "\n")
                file.close()
                tag = 0
                print("*" * 30)
                print("数据错误，已保存至txt！！！！！！")
                print("*" * 30)
            tag += 1
            # 保存queueHref和endHref
            pd.to_pickle(queueHref, "./queueHref.pkl")
            pd.to_pickle(endHref, "./endHref.pkl")
            # 读取queueHref和endHref
            endHref = pd.read_pickle("./endHref.pkl")
            queueHref = pd.read_pickle("./queueHref.pkl")
            # 发生错误的时间
            zTime = time.time()
            print("*" * 30)
            print("已用时：" + str(zTime - startTime) + "秒！！")
            print("发生错误，程序10秒后自动开始运行，！！！！！！")
            print("*" * 30)
            time.sleep(10)

    # 程序运行完的时间
    endTime = time.time()
    print("※" * 30)
    print("总用时：" + str(endTime - startTime) + "秒！！")
    print("爬取完成！！")
    print("※" * 30)


if __name__ == "__main__":
    crawl()