import requests
import re
from lxml import etree
from bs4 import BeautifulSoup

def getgamelink(url,s):
    gamelink_group = []
    myheaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    start_page = int(input('请输入要提取的起始页数：'))
    end_page = int(input('请输入要提取的结束页数：'))
    for page in range(start_page,end_page + 1):
        temp_url = url + str(page)
        response = s.get(temp_url,headers=myheaders)
        gamelink_list = re.compile('taptap-link" href="(.*?)" data-taptap-url').findall(response.text)
        # print(gamelink_list)
        # with open('temp.html','wb') as fp:
        #     fp.write(response.content)
        gamelink_group.extend(gamelink_list)
    return gamelink_group

def getgamename(gamelink_list,s):
    name_list = []
    for link in gamelink_list:
        detal_resp = s.get(link)
        tree = etree.HTML(detal_resp.content)
        name = tree.xpath('//h1[@itemprop="name"]/text()')
        # soup = BeautifulSoup(detal_resp,'lxml')
        # soup.select()
        name_result = str(name[0]).replace(' ','')
        name_list.append(name_result)
    return name_list


def main():
    s = requests.Session()
    main_url = 'https://www.taptap.com/category/hot?page='
    gamelink_list = getgamelink(main_url,s)
    name_list = getgamename(gamelink_list,s)
    print(gamelink_list,name_list)

if __name__ == "__main__":
    main()