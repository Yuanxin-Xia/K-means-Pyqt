from PyQt5.QtCore import QSize, QUrl, QRect
from PyQt5.QtWidgets import QToolBar, QMainWindow, QLineEdit, QPushButton, QMessageBox, QLabel, QDialog, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


from sys import exit, argv

from random import randint

import run_and_draw
import trans_address_to_lalo
import resource

class UI(QMainWindow, ):

    def __init__(self):
        super(UI, self).__init__()
        self.setWindowTitle('国内城市旅行规划')
        self.resize(1000, 1000)
        self.setFixedSize(1000, 1000)
        self.setWindowIcon(QIcon(':/icon.png'))
        self.setStyleSheet('QWidget{background-color:white}')

        # 浏览器窗口
        self.browser = QWebEngineView(self)
        self.browser.setGeometry(0, 0, 1000, 1000)
        self.zoom = 10
        self.lontitude = 102.672914
        self.latitude = 24.854418
        self.Latitude = []
        self.center = []


        # self.mark = '&markers='
        self.mark = ''
        # self.X = 'mid,0x'+color+',1:103.272914,24.754418;103.382904,25.098624;103.187825,26.082873;103.290785,24.771798;103.290785,24.771798;103.324432,24.8122|'
        self.X = ''
        color = "%06x" % randint(0, 0xFFFFFF)
        self.Y = ''
        # self.Y = 'mid,0x'+color+',2:102.665546,24.960582;102.666754,24.964496;102.665546,24.960582;102.664376,25.038297;102.640854,24.956885;102.671114,25.023184;102.668468,24.966766;102.659138,24.960492;102.6655,24.9598;102.651073,24.973296'
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

        # 工具条
        self.main_toolbar = QToolBar(self)
        self.main_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(self.main_toolbar)

        # 添加按钮
        self.Zoomin_button = QAction(QIcon(':/ZoomIn.png'), '放大', self)
        self.Zoomout_button = QAction(QIcon(':/ZoomOut.png'), '缩小', self)

        self.Up_button = QAction(QIcon(':/Up.png'), '向上移动', self)
        self.Down_button = QAction(QIcon(':/Down.png'), '向下移动', self)
        self.Left_button = QAction(QIcon(':/Left.png'), '向左移动', self)
        self.Right_button = QAction(QIcon(':/Right.png'), '向右移动', self)
        # 添加文本框
        self.place_text = QLineEdit(self)
        self.place_text.setMaximumWidth(280)
        self.place_text.setPlaceholderText("请输入旅行的城市(省份)：")
        font = QFont()
        font.setFamily('楷体')  # 设置字体
        font.setBold(True)  # 设置粗体
        font.setPixelSize(15)
        font.setPointSize(12)
        self.place_text.setFont(font)
        # 添加按钮,调用trans_address_to_lalo函数
        self.Insertplace_button = QAction(QIcon(':/Enter.png'), '输入', self)
        # 添加文本框
        self.time_text = QLineEdit(self)
        self.time_text.setMaximumWidth(270)
        self.time_text.setPlaceholderText("请输入计划天数(次数)：")
        font = QFont()
        font.setFamily('楷体')  # 设置字体
        font.setBold(True)  # 设置粗体
        font.setPixelSize(15)
        font.setPointSize(12)
        self.time_text.setFont(font)
        # 添加按钮，调用run_and_draw函数
        self.Inserttime_button = QAction(QIcon(':/Enter.png'), '输入', self)

        # 添加按钮，绘图
        self.Submit = QPushButton(self)
        self.Submit.setStyleSheet(''' 
           QPushButton{font-size:25px; border-width:20px;color:white;background-color:rgb(30,111,255);}
           QPushButton:hover{font-size:25px; border-width:5px;color:white;background-color:rgb(83,145,255);border-radius:5px;}
           QPushButton:pressed{font-size:25px; border-width:5px;color:white;background-color:rgb(27,101,135);border-radius:5px;}
                                           ''')
        self.Submit.setText('提交计算(S)')

        # 添加按钮动作

        # 放大缩小，移动地图
        self.main_toolbar.addAction(self.Zoomin_button)
        self.main_toolbar.addAction(self.Zoomout_button)
        self.main_toolbar.addAction(self.Up_button)
        self.main_toolbar.addAction(self.Down_button)
        self.main_toolbar.addAction(self.Left_button)
        self.main_toolbar.addAction(self.Right_button)
        # 放大缩小，写入地点按钮
        self.main_toolbar.addWidget(self.place_text)
        self.main_toolbar.addAction(self.Insertplace_button)
        # 放大缩小，写入K_means算法的k
        self.main_toolbar.addWidget(self.time_text)
        self.main_toolbar.addAction(self.Inserttime_button)
        # 调用run_and_draw函数
        self.main_toolbar.addWidget(self.Submit)
        # 添加按钮函数

        self.Zoomin_button.triggered.connect(self.Zoomin)
        self.Zoomout_button.triggered.connect(self.Zoomout)
        self.Up_button.triggered.connect(self.Up)
        self.Down_button.triggered.connect(self.Down)
        self.Left_button.triggered.connect(self.Left)
        self.Right_button.triggered.connect(self.Right)

        self.Insertplace_button.triggered.connect(self.Insertplace)
        self.Inserttime_button.triggered.connect(self.Inserttime)

        self.Submit.pressed.connect(self.Upload)


    def Zoomin(self):
        self.zoom = self.zoom + 1
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Zoomout(self):
        self.zoom = self.zoom - 1
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Up(self):
        if self.zoom >= 10:
            self.latitude += 0.1
        elif self.zoom == 9:
            self.latitude += 0.3
        elif self.zoom == 8:
            self.latitude += 0.5
        elif self.zoom == 7:
            self.latitude += 0.7
        elif self.zoom == 6:
            self.latitude += 0.9
        else : self.latitude += 2
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Down(self):
        if self.zoom >= 10:
            self.latitude -= 0.1
        elif self.zoom == 9:
            self.latitude -= 0.3
        elif self.zoom == 8:
            self.latitude -= 0.5
        elif self.zoom == 7:
            self.latitude -= 0.7
        elif self.zoom == 6:
            self.latitude -= 0.9
        else:
            self.latitude -= 2
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Left(self):
        if self.zoom >= 10:
            self.lontitude -= 0.1
        elif self.zoom == 9:
            self.lontitude -= 0.3
        elif self.zoom == 8:
            self.lontitude -= 0.5
        elif self.zoom == 7:
            self.lontitude -= 0.7
        elif self.zoom == 6:
            self.lontitude -= 0.9
        else:
            self.lontitude -= 2
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Right(self):
        if self.zoom >= 10:
            self.lontitude += 0.1
        elif self.zoom == 9:
            self.lontitude += 0.3
        elif self.zoom == 8:
            self.lontitude += 0.5
        elif self.zoom == 7:
            self.lontitude += 0.7
        elif self.zoom == 6:
            self.lontitude += 0.9
        else:
            self.lontitude += 2
        Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
            self.latitude) + '&zoom=' + str(
            self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'
        self.browser.setUrl(QUrl(Url))

    def Insertplace(self):

        self.Latitude = []
        self.Longtitude =[]
        self.center = []
        self.other = []

        text = self.place_text.text()
        if not '\u4e00' <= text <= '\u9fa5':
            QMessageBox.information(self, '提示', '请输入汉字')
        # 这里应该再加一个字典，匹配输入是否是国内地名，程序鲁棒性不够
        else:
            QMessageBox.information(self, '提示', '即将进行爬虫与经纬度转换操作，请稍等，不要关闭')
            self.Latitude, self.Longtitude = trans_address_to_lalo.trans_address_to_lalo(self, text)
            QMessageBox.information(self, '提示', '转换完成，请输入计划天数')

    def Inserttime(self):
        if len(self.Latitude) == 0:
            QMessageBox.information(self, '提示', '请先完成前一项输入')
            print(len(self.time_text.text()))
        else:
            text = self.time_text.text()
            if text.isdigit() == False:
                QMessageBox.information(self, '提示', '请输入数字')
            elif not (1 <= int(text) <= 20):
                QMessageBox.information(self, '提示', '请输入20以内数字')
            else:
                self.center, self.other,self.lontitude,self.latitude = run_and_draw.run_and_draw(self.Latitude, self.Longtitude, int(text))
                QMessageBox.information(self, '提示', '收到，请提交计算')
    def Upload(self):
        if (len(self.time_text.text()) == 0) or (len(self.place_text.text())== 0 or (len(self.Latitude))==0 or len(self.center) == 0):
            QMessageBox.information(self, '提示', '请先输入并提交完毕前两项')
        else:
            self.mark = '&markers='
            self.X = ""
            self.Y = ""
            #处理其他点的数据
            Can = []
            for i in range(1, 20):
                Can.append("" + str(i) + ":")
            for ii in self.other:
                Can[ii[2]] += (";" + str(ii[1]) + "," + str(ii[0]))
            for j in range(int(self.time_text.text())):
                Can[j] = Can[j].replace(Can[j][2], "", 1)
                color = "%06x" % randint(0, 0xFFFFFF)
                self.X += 'mid,0x'+color+','+Can[j]+'|'
            self.X = self.X[:-1]
            '''
            # 处理中心点的数据
            Box = []
            for i in range(int(self.time_text.text())):
                Box.append("" + str(i) + ":" + str(self.center[i][0]) + "," + str(self.center[i][1]))
                color = '000000'
                self.Y += 'mid,0x' + color + ',' + Box[i] + '|'
            self.Y = self.Y[:-1]
            '''
            Url = 'https://restapi.amap.com/v3/staticmap?location=' + str(self.lontitude) + ',' + str(
                self.latitude) + '&zoom=' + str(
                self.zoom) + '&size=1000*1000' + self.mark + self.X + self.Y + '&key=e64e53102dc5f929aed6622db61f3167'

            self.browser.setUrl(QUrl(Url))


if __name__ == '__main__':
    app = QApplication(argv)
    gui = UI()
    gui.show()
    exit(app.exec_())
