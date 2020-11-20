import Crawler
import Getlnglat


def trans_address_to_lalo(self,city):
    latituede=[]
    longtitude=[]
    x,address= Crawler.SightSpider(self,city)
    for i in range(len(address)):#对地址文件进行循环
        #调用函数
        value = Getlnglat.getlnglat(address[i])
        if value == 0:#如果地址不存在，就跳过
            continue
        #解析数据并存入列表
        latituede.append(float(value[1]))
        longtitude.append(float(value[0]))
    print("[INFO]:景点经纬度转换完成")
    #self.chile_Win.textEdit.setPlainText('[INFO]:景点经纬度转换完成')
    return latituede,longtitude