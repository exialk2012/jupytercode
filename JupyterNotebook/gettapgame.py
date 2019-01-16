import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series,DataFrame

def getgamelink(url,s,myheaders):
    gamelink_group = []
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

def getgamename(gamelink_list,s,myheaders):
    name_list = []
    rating_list = []
    type_list = []
    for link in gamelink_list:
        detal_resp = s.get(link,headers=myheaders)
        tree = etree.HTML(detal_resp.content)
        name = tree.xpath('//h1[@itemprop="name"]/text()')
        rating_value = tree.xpath('//span[@itemprop="ratingValue"]/text()')
        author = tree.xpath('//div/div[@class="header-text-author"]//span[@itemprop="name"]/text()')
        gametype = tree.xpath('//ol[@class="breadcrumb"]/li/a[@href]/text()')
        # soup = BeautifulSoup(detal_resp,'lxml')
        # soup.select()
        name_result = str(name[0]).replace(' ','')
        name_list.append(name_result)
        rating_list.append(rating_value[0])
        type_list.append(gametype[1])
        # print(author)
    return name_list,rating_list,type_list

def getgamecount(gamelinke_list,s,myheaders):
    install_list = []
    guanzhu_list = []
    for link in gamelinke_list:
        detal_resp = s.get(link,headers=myheaders)
        tree = etree.HTML(detal_resp.content)
        gamecount = tree.xpath('//span[@class="count-stats"]/text()')
        if len(gamecount) == 2:
            install_count = re.sub('\D','',gamecount[0])
            guanzhu_count = re.sub('\D','',gamecount[1])
            install_list.append(install_count)
            guanzhu_list.append(guanzhu_count)
            # print('安装人数：'+ str(install_count))
            # print('关注人数：'+ str(guanzhu_count))
        else:
            install_count = str(0)
            guanzhu_count = re.sub('\D','',gamecount[0])
            install_list.append(install_count)
            guanzhu_list.append(guanzhu_count)
            # print('安装人数：'+ str(install_count))
            # print('关注人数：'+ str(guanzhu_count))
    return install_list,guanzhu_list



def main():
    s = requests.Session()
    myheaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    main_url = 'https://www.taptap.com/category/hot?page='
    gamelink_list = getgamelink(main_url,s,myheaders)
    
    name_list,rating_list,type_list = getgamename(gamelink_list,s,myheaders)
    install_list,guanzhu_list = getgamecount(gamelink_list,s,myheaders)
    game_data = {
        '游戏名称':name_list,
        '游戏评分':rating_list,
        '游戏类型':type_list,
        '安装、预约、购买人数':install_list,
        '关注人数':guanzhu_list,
    }

    game_data_df = DataFrame(game_data)
    game_data_df.to_excel('taptaphot.xlsx',sheet_name='gamedata')
    # print(game_data)

if __name__ == "__main__":
    main()