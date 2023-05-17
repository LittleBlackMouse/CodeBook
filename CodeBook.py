# _*_ coding:utf-8 _*_
# 程序名称：密码本
# 版本：v1.0
# 编写日期：2023-05-02
# 作者：Big Mouse
import os
import shutil
import sys
import uuid
import Encryption as Ep
import Decryption as Dp
import base64

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem, QAbstractItemView
from CodeBookLogin import Ui_Form  # 导入登录窗口模块
from CodeBookMain import Ui_Form as Main_Form  # 导入主页面窗口模块


# 创建主程序窗口
class MainWin(QWidget, Main_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showTable()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止表格编辑
        self.lineEdit_3.setHidden(True)  # 隐藏控件
        self.pushButton.clicked.connect(self.informationEntry)
        self.pushButton_3.clicked.connect(self.modifyInformation)
        self.pushButton_5.clicked.connect(self.accountDelete)
        self.pushButton_2.clicked.connect(self.selectInformation)
        self.comboBox_2.currentIndexChanged.connect(self.changeHide)
        self.pushButton_6.clicked.connect(self.showTable)

    def changeHide(self):
        """
        改变line3和cbox3的显隐状态
        :return:
        """
        index = self.comboBox_2.currentIndex()
        if index == 0:
            self.comboBox_3.setHidden(False)
            self.lineEdit_3.setHidden(True)
        else:
            self.comboBox_3.setHidden(True)
            self.lineEdit_3.setHidden(False)

    def selectInformation(self):
        """
        存储账号信息查询
        :return:
        """
        index = self.comboBox_2.currentIndex()
        text = self.lineEdit_3.text()
        if index == 0:
            form_text = self.comboBox_3.currentText()
            form_text_base = str(base64.b64encode(form_text.encode()))[2:-1]  # 将字符转换成base64格式
            # 遍历文件夹下所有文件夹名称
            filename_list = []
            for dirpath, dirnames, filenames in os.walk(f'./folder/{accout_id}/{form_text_base}'):
                for filename in filenames:
                    filename_list.append(filename)
            # 清空表中数据
            row_num = self.tableWidget.rowCount()
            while row_num >= 0:
                self.tableWidget.removeRow(row_num)
                row_num -= 1
            if filename_list:
                for filename in filename_list:
                    self.tableWidget.insertRow(0)
                    get_acot = Dp.decrypt(f'./folder/{accout_id}/{form_text_base}/', filename, filename, 'parent')
                    get_pws = Dp.decrypt(f'./folder/{accout_id}/{form_text_base}/', filename, filename, 'child')
                    items = [[form_text, get_acot, get_pws]]
                    self.tableWidget.setItem(0, 0, QTableWidgetItem(str(items[0][0])))
                    self.tableWidget.setItem(0, 1, QTableWidgetItem(str(items[0][1])))
                    self.tableWidget.setItem(0, 2, QTableWidgetItem(str(items[0][2])))
        elif text:
            # 遍历文件夹下所有文件夹名称
            folder_list = []
            for dirpath, dirnames, filenames in os.walk(f'./folder/{accout_id}'):
                for dirname in dirnames:
                    if dirname != accout_id:
                        folder_list.append(dirname)
            # 判断文件夹是否为空
            if folder_list:
                # 清空表中数据
                row_num = self.tableWidget.rowCount()
                while row_num >= 0:
                    self.tableWidget.removeRow(row_num)
                    row_num -= 1
                # 清空类型下拉框数据
                self.comboBox.clear()
                self.comboBox_3.clear()
                # 遍历文件夹名称
                for folder_name in folder_list:
                    # 账户信息-账户类型
                    form_type = base64.b64decode(folder_name.encode()).decode()
                    self.comboBox.addItem(form_type)
                    self.comboBox_3.addItem(form_type)
                    # 遍历文件夹内的所有文件信息
                    for root, dirs, files in os.walk(f'./folder/{accout_id}/{folder_name}'):
                        for file in files:
                            get_acot = Dp.decrypt(f'./folder/{accout_id}/{folder_name}/', file, file, 'parent')
                            get_pws = Dp.decrypt(f'./folder/{accout_id}/{folder_name}/', file, file, 'child')
                            if (get_acot == text and index == 1) or (get_pws == text and index == 2):
                                self.tableWidget.insertRow(0)
                                items = [[form_type, get_acot, get_pws]]
                                self.tableWidget.setItem(0, 0, QTableWidgetItem(str(items[0][0])))
                                self.tableWidget.setItem(0, 1, QTableWidgetItem(str(items[0][1])))
                                self.tableWidget.setItem(0, 2, QTableWidgetItem(str(items[0][2])))
        else:
            self.erroMsg('输入的查询信息为空！')

    def modifyInformation(self):
        """
        修改账户信息
        :return:
        """
        # 读取输入框信息
        form = self.comboBox.currentText()
        accout = self.lineEdit.text()
        pws = self.lineEdit_2.text()
        if form and accout and pws:
            form_base = str(base64.b64encode(form.encode()))[2:-1]  # 将字符转换成base64格式
            try:
                # 遍历文件夹下所有文件夹名称
                folder_list = []
                act_list = []
                for dirpath, dirnames, filenames in os.walk(f'./folder/{accout_id}/{form_base}'):
                    for filename in filenames:
                        folder_list.append(filename)
                for act_id in folder_list:
                    get_act = Dp.decrypt(f'./folder/{accout_id}/{form_base}/', act_id, act_id, 'parent')
                    act_list.append([act_id, get_act])
                num = 0
                for act in act_list:
                    num += 1
                    if accout in act:
                        path = f'./folder/{accout_id}/{form_base}/{act[0]}'
                        os.remove(path)
                        self.informationEntry()
                        self.showTable()
                        break
                    elif num == len(act_list):
                        self.erroMsg(f'【{form}】类型中，该账号不存在！')
            except Exception as ec:
                self.erroMsg(str(ec))
        else:
            self.erroMsg('类型、账号或密码为空！')

    def accountDelete(self):
        """
        删除账号信息
        :return:
        """
        # 读取输入框信息
        form = self.comboBox.currentText()
        accout = self.lineEdit.text()
        if form and accout:
            form_base = str(base64.b64encode(form.encode()))[2:-1]  # 将字符转换成base64格式
            try:
                # 遍历文件夹下所有文件夹名称
                folder_list = []
                act_list = []
                for dirpath, dirnames, filenames in os.walk(f'./folder/{accout_id}/{form_base}'):
                    for filename in filenames:
                        folder_list.append(filename)
                for act_id in folder_list:
                    get_act = Dp.decrypt(f'./folder/{accout_id}/{form_base}/', act_id, act_id, 'parent')
                    act_list.append([act_id, get_act])
                num = 0
                for act in act_list:
                    num += 1
                    if accout in act:
                        path = f'./folder/{accout_id}/{form_base}/{act[0]}'
                        os.remove(path)
                        self.erroMsg('账号已删除！')
                        self.showTable()
                        break
                    elif num == len(act_list):
                        self.erroMsg(f'【{form}】类型中，该账号不存在！')
            except Exception as ec:
                self.erroMsg(str(ec))
        else:
            self.erroMsg('类型或账号为空！')

    def showTable(self):
        """
        从本地文件获取文件信息
        并在表中展示
        :return:
        """
        # 遍历文件夹下所有文件夹名称
        folder_list = []
        for dirpath, dirnames, filenames in os.walk(f'./folder/{accout_id}'):
            for dirname in dirnames:
                if dirname != accout_id:
                    folder_list.append(dirname)
        # 判断文件夹是否为空
        if folder_list:
            # 清空表中数据
            row_num = self.tableWidget.rowCount()
            while row_num >= 0:
                self.tableWidget.removeRow(row_num)
                row_num -= 1
            # 清空类型下拉框数据
            self.comboBox.clear()
            self.comboBox_3.clear()
            # 遍历文件夹名称
            for folder_name in folder_list:
                # 账户信息-账户类型
                form_type = base64.b64decode(folder_name.encode()).decode()
                self.comboBox.addItem(form_type)
                self.comboBox_3.addItem(form_type)
                # 遍历文件夹内的所有文件信息
                for root, dirs, files in os.walk(f'./folder/{accout_id}/{folder_name}'):
                    for file in files:
                        self.tableWidget.insertRow(0)
                        get_acot = Dp.decrypt(f'./folder/{accout_id}/{folder_name}/', file, file, 'parent')
                        get_pws = Dp.decrypt(f'./folder/{accout_id}/{folder_name}/', file, file, 'child')
                        items = [[form_type, get_acot, get_pws]]
                        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(items[0][0])))
                        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(items[0][1])))
                        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(items[0][2])))

    def informationEntry(self):
        """
        信息录入
        :return:
        """
        # 读取输入框信息
        form = self.comboBox.currentText()
        accout = self.lineEdit.text()
        pws = self.lineEdit_2.text()
        if form and accout and pws:
            # 获取
            id = uuid.uuid1()
            id = str(id).replace('-', '')
            form_base = str(base64.b64encode(form.encode()))[2:-1]
            # 判断文件夹是否存在，否则创建文件夹
            path_dir = f'./folder/{accout_id}/{form_base}'
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            # 将录入信息加密存储
            acot_rest = Ep.encryption(f'./folder/{accout_id}/{form_base}/', id, accout, id, 'parent')
            pws_rest = Ep.encryption(f'./folder/{accout_id}/{form_base}/', id, pws, id, 'child')
            # 判断文件是否保存成功
            if acot_rest == 'save success!' and pws_rest == 'save success!':
                self.erroMsg('录入成功！')
                self.showTable()
            else:
                self.erroMsg('录入失败！')
        else:
            self.erroMsg('类型、账号、或密码为空！')

    def erroMsg(self, err_msg):
        """
        错误信息提示框
        :return:
        """
        QMessageBox.information(self, 'CodeBook', err_msg)

    # 重写鼠标移动窗口函数
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


# 创建登录窗口
class LoginWin(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.ui = None  # 定义一个空变量用于后面存放主窗口
        self.setupUi(self)
        # 隐藏自带窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton.clicked.connect(self.switchWindow)  # 登录到主窗口
        self.lineEdit_2.returnPressed.connect(self.switchWindow)  # 输入完密码回车登录
        self.pushButton_2.clicked.connect(self.registerAccount)  # 注册账号

    def switchWindow(self):
        """
        登录成功时切换至主窗口
        :return:
        """
        # 获取输入账号密码信息
        user = self.lineEdit.text()
        psw = self.lineEdit_2.text()
        # 当账号密码正确时跳转窗口
        if user and psw:
            # 遍历文件夹下所有文件夹名称
            folder_list = []
            for dirpath, dirnames, filenames in os.walk('./folder'):
                for dirname in dirnames:
                    if dirpath == './folder':
                        folder_list.append(dirname)
            # 判断文件夹是否为空
            if folder_list:
                acot_dict = dict()
                # 遍历文件夹名称
                for folder_name in folder_list:
                    get_acot = Dp.decrypt(f'./folder/{folder_name}/', folder_name, folder_name, 'parent')
                    get_pws = Dp.decrypt(f'./folder/{folder_name}/', folder_name, folder_name, 'child')
                    acot_dict.update({get_acot: [get_pws, folder_name]})
                if user in acot_dict.keys():
                    if psw == acot_dict[user][0]:
                        global accout_id
                        accout_id = acot_dict[user][1]
                        self.ui = MainWin()  # 实例化主窗口程序
                        # 隐藏自带窗口
                        self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                        self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                        self.ui.show()  # 显示主窗口
                        self.hide()  # 隐藏登录窗口
                        self.ui.pushButton_4.clicked.connect(self.showHide)  # 关闭窗口时返回登录窗口
                    else:
                        self.erroMsg('密码错误！')
                else:
                    self.erroMsg('账号不存在！')
        else:
            self.erroMsg('账号或密码为空！')

    def registerAccount(self):
        """
        注册账号
        :return:
        """
        # 获取账号密码框是否为空
        acot = self.lineEdit.text()
        pws = self.lineEdit_2.text()
        if acot and pws:
            # 遍历文件夹下所有文件夹名称
            folder_list = []
            for dirpath, dirnames, filenames in os.walk('./folder'):
                if dirpath == './folder':
                    for dirname in dirnames:
                        folder_list.append(dirname)
            jif = 0
            # 判断文件夹是否为空
            if folder_list:
                # 遍历文件夹名称
                for folder_name in folder_list:
                    get_acot = Dp.decrypt(f'./folder/{folder_name}/', folder_name, folder_name, 'parent')
                    if acot == get_acot:
                        self.erroMsg('账号已注册，请直接登录')
                        break
                    else:
                        jif += 1
            if jif == len(folder_list):
                # 获取
                id = uuid.uuid1()
                id = str(id).replace('-', '')
                # 创建文件夹
                os.makedirs(f'./folder/{id}')
                # 文件加密写入
                acot_rest = Ep.encryption(f'./folder/{id}/', id, acot, id, 'parent')
                pws_rest = Ep.encryption(f'./folder/{id}/', id, pws, id, 'child')
                # 判断文件是否保存成功
                if acot_rest == 'save success!' and pws_rest == 'save success!':
                    self.erroMsg('账号注册成功！')
                else:
                    try:
                        shutil.rmtree(f'./folder/{id}')
                    except Exception as ec:
                        self.erroMsg(str(ec))
                    self.erroMsg('注册失败！')
        else:
            self.erroMsg('账号或密码为空！')

    # 重写鼠标移动窗口函数
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def showHide(self):
        """
        重新显示登录窗口,
        不保留原有的登录信息
        :return:
        """
        # 清除原有填写的账号密码信息
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        # 重新显示主窗口
        self.show()

    def erroMsg(self, err_msg):
        """
        错误信息提示框
        :return:
        """
        QMessageBox.information(self, 'CodeBook', err_msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    path_dir = './folder'
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    win = LoginWin()
    win.show()
    sys.exit(app.exec_())
