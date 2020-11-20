from requests import get
from bs4 import BeautifulSoup
from time import sleep
from re import findall
from urllib.parse import quote


'''携程国内旅游景点爬虫'''
def SightSpider(self,city):
        info = get_city_and_index(city)[0]
        print('[INFO]:正在爬取'+city+'景点信息....')
        #构造请求头和请求url
        headers = {'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        url = 'https://you.ctrip.com/sight/'+info+'/s0-p%s.html#sightname'
        #爬取网页页数
        max_pages = 3
        max_pages +=1
        page_count = 1
        spots = []
        locates =[]
        while True:
                #发送request的get请求，获得旅游页面响应
                res = get(url % page_count, headers=headers)
                #使用bs4解析库解析响应页面
                soup = BeautifulSoup(res.text, features='lxml')
                if soup.find_all('div', class_='list_wide_mod2') == []:
                    print("[INFO]:已经没有景点啦！")  
                    return spots,locates
                list_wide_mod2 = soup.find_all('div', class_='list_wide_mod2')[0]
                for each1, each2,each3 in zip(list_wide_mod2.find_all('dl'), list_wide_mod2.find_all('ul', class_='r_comment'),list_wide_mod2.find_all('p', class_='bottomcomment')):
                        #获得景点名称
                        name = each1.dt.a.text
                        spots.append(name)
                        #获得景点地址
                        addr = each1.find_all('dd')[0].text.strip()
                        locates.append(addr)
                page_count += 1
                #self.chile_Win.textEdit.setPlainText('[INFO]:爬取进度: %s/%s...' % (page_count-1, max_pages-1))
                print('[INFO]:爬取进度: %s/%s...' % (page_count-1, max_pages-1))
                sleep(0.5)
                if page_count == max_pages:
                        return spots,locates
                
"""返回当前城市或省份的拼音和携程网代号"""
def get_city_and_index(city): 
    add = quote(city)
    #构造请求头和请求url
    url="https://you.ctrip.com/searchsite/?query="+add
    headers = {'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    res = get(url, headers=headers)
    #使用bs4解析库解析响应页面
    soup = BeautifulSoup(res.text, features='lxml')
    list_wide_mod2 = soup.find_all('li', class_='cf')[0]
    string = str(list_wide_mod2.find_all('a')[0].get_text)
    local = findall(r'place/(.*).html', string)
    return local