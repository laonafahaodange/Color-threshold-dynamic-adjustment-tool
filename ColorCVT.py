from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv
from PyQt5.QtWidgets import *
from ColorCVT_UI import *
import numpy as np
import sys

# 原图数据
img_original = None
# 判断radiobutton的标志位
hsv_flag = False
hls_flag = False
# 阈值
hsv_min = np.array([0, 0, 0])
hsv_max = np.array([255, 255, 255])
hls_min = np.array([0, 0, 0])
hls_max = np.array([255, 255, 255])


class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # 界面初始化以及事件绑定
        self.img_select_pushButton.clicked.connect(self.select_img)
        self.hsv_radioButton.toggled.connect(self.hsv_img)
        self.hls_radioButton.toggled.connect(self.hls_img)
        self.hsv_radioButton.setEnabled(False)
        self.hls_radioButton.setEnabled(False)
        self.c1_l_horizontalSlider.setEnabled(False)
        self.c1_h_horizontalSlider.setEnabled(False)
        self.c2_l_horizontalSlider.setEnabled(False)
        self.c2_h_horizontalSlider.setEnabled(False)
        self.c3_l_horizontalSlider.setEnabled(False)
        self.c3_h_horizontalSlider.setEnabled(False)
        self.slider_init()
        self.c1_l_horizontalSlider.valueChanged.connect(self.c1_l_valuechange)
        self.c1_h_horizontalSlider.valueChanged.connect(self.c1_h_valuechange)
        self.c2_l_horizontalSlider.valueChanged.connect(self.c2_l_valuechange)
        self.c2_h_horizontalSlider.valueChanged.connect(self.c2_h_valuechange)
        self.c3_l_horizontalSlider.valueChanged.connect(self.c3_l_valuechange)
        self.c3_h_horizontalSlider.valueChanged.connect(self.c3_h_valuechange)

    # 尝试调用cv.inRange方法但是在pyqt5下一直出现崩溃情况，无奈根据inRange原理重写其实现
    # 原理其实是将每个通道内介于阈值之间的像素值赋值255（关于等于阈值的情况我没有深究，仍然将其赋值255），其余赋值为0
    # QImage模块没有HSV以及HLS格式，所以只能调用OpenCV的imshow方法，原本是想显示在img_label上的...
    def update_img(self):
        global img_original
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        # HSV
        if hsv_flag is True and hls_flag is False:
            hsv_img = cv.cvtColor(img_original, cv.COLOR_BGR2HSV)
            h = hsv_img[:, :, 0]
            h_bin = np.zeros_like(h)
            h_bin[(h >= hsv_min[0]) & (h <= hsv_max[0])] = 255

            s = hsv_img[:, :, 1]
            s_bin = np.zeros_like(s)
            s_bin[(s >= hsv_min[1]) & (s <= hsv_max[1])] = 255

            v = hsv_img[:, :, 2]
            v_bin = np.zeros_like(v)
            v_bin[(v >= hsv_min[2]) & (v <= hsv_max[2])] = 255

            # 二值化只需要一个通道，这里随便取其中一个通道
            hsv_bin = np.zeros_like(h)
            hsv_bin[(h_bin == 255) & (s_bin == 255) & (v_bin == 255)] = 255
            cv.imshow('HSV_img', hsv_bin)
        # HLS
        elif hsv_flag is False and hls_flag is True:
            hls_img = cv.cvtColor(img_original, cv.COLOR_BGR2HLS)
            h = hls_img[:, :, 0]
            h_bin = np.zeros_like(h)
            h_bin[(h >= hls_min[0]) & (h <= hls_max[0])] = 255

            l = hls_img[:, :, 1]
            l_bin = np.zeros_like(l)
            l_bin[(l >= hls_min[1]) & (l <= hls_min[1])] = 255

            s = hls_img[:, :, 2]
            s_bin = np.zeros_like(s)
            s_bin[(s >= hls_min[2]) & (s <= hls_min[2])] = 255

            # 二值化只需要一个通道，这里随便取其中一个通道
            hls_bin = np.zeros_like(h)
            hls_bin[(h_bin == 255) & (l_bin == 255) & (s_bin == 255)] = 255
            cv.imshow('HLS_img', hls_bin)

    # slider的逻辑
    def c1_l_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c1_l_label.setText('H min: ' + str(self.c1_l_horizontalSlider.value()))
            hsv_min[0] = np.int(self.c1_l_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c1_l_label.setText('H min: ' + str(self.c1_l_horizontalSlider.value()))
            hls_min[0] = np.int(self.c1_l_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    def c1_h_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c1_h_label.setText('H max: ' + str(self.c1_h_horizontalSlider.value()))
            hsv_max[0] = np.int(self.c1_h_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c1_h_label.setText('H max: ' + str(self.c1_h_horizontalSlider.value()))
            hls_max[0] = np.int(self.c1_h_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    def c2_l_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c2_l_label.setText('S min: ' + str(self.c2_l_horizontalSlider.value()))
            hsv_min[1] = np.int(self.c2_l_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c2_l_label.setText('L min: ' + str(self.c2_l_horizontalSlider.value()))
            hls_min[1] = np.int(self.c2_l_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    def c2_h_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c2_h_label.setText('S max: ' + str(self.c2_h_horizontalSlider.value()))
            hsv_max[1] = np.int(self.c2_h_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c2_h_label.setText('L max: ' + str(self.c2_h_horizontalSlider.value()))
            hls_max[1] = np.int(self.c2_h_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    def c3_l_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c3_l_label.setText('V min: ' + str(self.c3_l_horizontalSlider.value()))
            hsv_min[2] = np.int(self.c3_l_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c3_l_label.setText('S min: ' + str(self.c3_l_horizontalSlider.value()))
            hls_min[2] = np.int(self.c3_l_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    def c3_h_valuechange(self):
        global hsv_flag, hls_flag
        global hsv_min, hsv_max, hls_min, hls_max
        if hsv_flag is True and hls_flag is False:
            self.c3_h_label.setText('V max: ' + str(self.c3_h_horizontalSlider.value()))
            hsv_max[2] = np.int(self.c3_h_horizontalSlider.value())
            self.textEdit.setText('hsv_min=' + str(hsv_min) + '\n' + 'hsv_max=' + str(hsv_max))
            self.update_img()
        elif hsv_flag is False and hls_flag is True:
            self.c3_h_label.setText('S max: ' + str(self.c3_h_horizontalSlider.value()))
            hls_max[2] = np.int(self.c3_h_horizontalSlider.value())
            self.textEdit.setText('hls_min=' + str(hls_min) + '\n' + 'hls_max=' + str(hls_max))
            self.update_img()

    # slider初始化
    def slider_init(self):
        global hsv_min, hsv_max, hls_min, hls_max
        hsv_min = [0, 0, 0]
        hsv_max = [255, 255, 255]
        hls_min = [0, 0, 0]
        hls_max = [255, 255, 255]

        self.c1_l_horizontalSlider.setMinimum(0)
        self.c1_l_horizontalSlider.setMaximum(255)
        self.c1_h_horizontalSlider.setMinimum(0)
        self.c1_h_horizontalSlider.setMaximum(255)
        self.c2_l_horizontalSlider.setMinimum(0)
        self.c2_l_horizontalSlider.setMaximum(255)
        self.c2_h_horizontalSlider.setMinimum(0)
        self.c2_h_horizontalSlider.setMaximum(255)
        self.c3_l_horizontalSlider.setMinimum(0)
        self.c3_l_horizontalSlider.setMaximum(255)
        self.c3_h_horizontalSlider.setMinimum(0)
        self.c3_h_horizontalSlider.setMaximum(255)

        self.c1_l_horizontalSlider.setSingleStep(1)
        self.c1_l_horizontalSlider.setSingleStep(1)
        self.c1_h_horizontalSlider.setSingleStep(1)
        self.c1_h_horizontalSlider.setSingleStep(1)
        self.c2_l_horizontalSlider.setSingleStep(1)
        self.c2_l_horizontalSlider.setSingleStep(1)
        self.c2_h_horizontalSlider.setSingleStep(1)
        self.c2_h_horizontalSlider.setSingleStep(1)
        self.c3_l_horizontalSlider.setSingleStep(1)
        self.c3_l_horizontalSlider.setSingleStep(1)
        self.c3_h_horizontalSlider.setSingleStep(1)
        self.c3_h_horizontalSlider.setSingleStep(1)

        self.c1_l_horizontalSlider.setValue(0)
        self.c1_h_horizontalSlider.setValue(255)
        self.c2_l_horizontalSlider.setValue(0)
        self.c2_h_horizontalSlider.setValue(255)
        self.c3_l_horizontalSlider.setValue(0)
        self.c3_h_horizontalSlider.setValue(255)

        self.c1_l_label.setText(str(self.c1_l_horizontalSlider.value()))
        self.c1_h_label.setText(str(self.c1_h_horizontalSlider.value()))
        self.c2_l_label.setText(str(self.c1_l_horizontalSlider.value()))
        self.c2_h_label.setText(str(self.c1_h_horizontalSlider.value()))
        self.c3_l_label.setText(str(self.c1_l_horizontalSlider.value()))
        self.c3_h_label.setText(str(self.c1_h_horizontalSlider.value()))

    # 显示图像在QT上，QImage支持显示的图像颜色空间格式不多...
    def display_img(self, img):
        rows, cols, channels = img.shape
        bytesPerLine = channels * cols
        qt_img = QImage(img.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        img = QtGui.QPixmap(qt_img).scaled(self.img_label.width(), self.img_label.height())
        self.img_label.setPixmap(img)
        self.img_label.setScaledContents(True)

    # 选择图片的逻辑
    def select_img(self):
        try:
            global img_original
            img_name, img_type = QFileDialog.getOpenFileName(self, '选择图片', '', '*.jpg;; *.png;;ALL files(*)')
            # 上一次打开过图片，这一次点击选择图片但是点取消的逻辑部分
            # print(img_name)
            if img_name == '':
                img_original = img_original
            else:
                img_original = cv.imread(img_name)
            img = cv.cvtColor(img_original, cv.COLOR_BGR2RGB)
            cv.destroyAllWindows()
            self.display_img(img)
            self.hsv_radioButton.setEnabled(True)
            self.hls_radioButton.setEnabled(True)
        except:
            return

    # radiobutton的逻辑
    def hsv_img(self):
        global img_original
        global hsv_flag
        global hls_flag
        if img_original is None:
            return
        else:
            hsv_flag = True
            hls_flag = False
            cv.destroyAllWindows()
            cv.namedWindow('HSV_img', cv.WINDOW_NORMAL)
            self.update_img()
        self.slider_init()
        self.c1_l_horizontalSlider.setEnabled(True)
        self.c1_h_horizontalSlider.setEnabled(True)
        self.c2_l_horizontalSlider.setEnabled(True)
        self.c2_h_horizontalSlider.setEnabled(True)
        self.c3_l_horizontalSlider.setEnabled(True)
        self.c3_h_horizontalSlider.setEnabled(True)

    def hls_img(self):
        global img_original
        global hsv_flag
        global hls_flag
        if img_original is None:
            return
        else:
            hsv_flag = False
            hls_flag = True
            cv.destroyAllWindows()
            cv.namedWindow('HLS_img', cv.WINDOW_NORMAL)
        self.slider_init()
        self.c1_l_horizontalSlider.setEnabled(True)
        self.c1_h_horizontalSlider.setEnabled(True)
        self.c2_l_horizontalSlider.setEnabled(True)
        self.c2_h_horizontalSlider.setEnabled(True)
        self.c3_l_horizontalSlider.setEnabled(True)
        self.c3_h_horizontalSlider.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
    cv.destroyAllWindows()

    # 测试
    # img_original = cv.imread('D:/project/python_pro/graduation_project/tools/icon.jpg')
    # hsv_img = cv.cvtColor(img_original, cv.COLOR_BGR2HSV)
    # print(hsv_img.shape)
    # hsv_img = cv.inRange(hsv_img, hsv_min, hsv_max)
    # cv.namedWindow('HSV_img', cv.WINDOW_NORMAL)
    # cv.imshow('HSV_img', hsv_img)
    # cv.waitKey(0)
