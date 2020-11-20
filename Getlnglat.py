from requests import get
from time import sleep

'''
函数的参数为api密钥和城市名,返回值为当前网页XML
'''

def getlnglat(address):
    parameters = {'address': address, 'key': 'e64e53102dc5f929aed6622db61f3167'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = get(base, parameters)
    answer = response.json()
    sleep(0.5)
    if (answer.get('geocodes') == []):   #如果没有这个地点
        locate = 0
    else: 
        locate = answer['geocodes'][0]['location'].split(",")    
    return locate
