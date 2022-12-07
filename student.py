#-coding:gb2312-*-
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string
import psycopg2
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QDateTime, QDate, QTime
from PyQt5.QtGui import QMouseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QMenu, QAction, QVBoxLayout, \
    QTableWidgetItem, QLCDNumber
from PyQt5.uic.properties import QtWidgets, QtCore

from enrollment import Ui_mainWindow
from register import Ui_MainWindow as Ui_mainWindow_reg
from subject import Ui_MainWindow as Ui_mainWindow_sub
from quiz import Ui_MainWindow as Ui_mainWindow_quiz
from new_pw import Ui_MainWindow as Ui_mainWindow_pw
from manage import Ui_MainWindow as Ui_mainWindow_m



class Student(QMainWindow,Ui_mainWindow):
    def __init__(self):
        super(Student, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.btn_connect()

        self.initUi()


    def initUi(self):
        self.createTrayIcon()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        # 让托盘图标显示在系统托盘上
        self.trayIcon.show()
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 窗口置顶，无边框，在任务栏不显示图标
        self.setWindowFlags(Qt.FramelessWindowHint)

    # 创建托盘图标
    def createTrayIcon(self):
        aRestore = QAction('恢复(&R)', self, triggered=self.showNormal)
        aQuit = QAction('退出(&Q)', self, triggered=QApplication.instance().quit)
        menu = QMenu(self)
        menu.addAction(aRestore)
        menu.addAction(aQuit)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)

    def btn_connect(self):
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)
        self.pushButton.clicked.connect(self.enroll)
        self.pushButton_8.clicked.connect(self.email)
        self.pushButton_2.clicked.connect(self.regist)

    def regist(self):
        self.hide()
        regist.show()

    def email(self):
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, "提示", "请输入用户名！" )
        else:
            npw.show()
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            if self.radioButton.isChecked():
                self.cur.execute('select * from student')  # 将数据从数据库中拿出来
            else:
                self.cur.execute('select * from teacher')
            self.total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
            self.cur.execute(f"select semail from student where susername='{self.lineEdit.text()}'")
            email = self.cur.fetchone()
            print(email[0])
            # 创建 SMTP 对象
            smtp = smtplib.SMTP()
            # 连接（connect）指定服务器
            smtp.connect("smtp.126.com", port=25)
            # 登录，需要：登录邮箱和授权码
            smtp.login(user="python_zsh@126.com", password="WBPWOWBLWIUJZRLN")
            pw_list = random.sample(string.ascii_letters + string.digits, 9)
            pw = 'z'
            for i in pw_list:
                pw += i
            print(pw)
            # 构造MIMEText对象，参数为：正文，MIME的subtype，编码方式
            message = MIMEText(f'初始化密码：{pw}', 'plain', 'utf-8')
            message['From'] = Header("z")  # 发件人的昵称
            message['To'] = Header("your")  # 收件人的昵称
            message['Subject'] = Header('在线考试系统修改密码', 'utf-8')  # 定义主题内容
            smtp.sendmail(from_addr="python_zsh@126.com", to_addrs=f"{email[0]}", msg=message.as_string())
            self.cur.execute(f"update student set spassword='{pw}' where susername='{self.lineEdit.text()}'")
            self.conn.commit()
            self.cur.close()
            self.conn.close()


    def enroll(self):
        if len(self.lineEdit.text())==0 or len(self.lineEdit_2.text())==0  :
            QMessageBox.information(self, "提示", "请填写用户名和密码！")
        elif self.radioButton.isChecked() == True :
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            self.cur.execute(f"select susername,spassword from student where susername='{self.lineEdit.text()}'")
            username_db = self.cur.fetchone()
            print(username_db)
            if username_db[1] != self.lineEdit_2.text():
                QMessageBox.information(self, "提示", "密码错误！")
            else:
                self.cur.close()
                self.conn.close()
                self.hide()
                sub.show()

        elif self.radioButton_2.isChecked() == True:
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            self.cur.execute(f"select tusername,tpassword from teacher where tusername='{self.lineEdit.text()}'")
            username_db = self.cur.fetchone()
            print(username_db)
            if username_db[1] != self.lineEdit_2.text():
                QMessageBox.information(self, "提示", "密码错误！")
            else:
                self.cur.close()
                self.conn.close()
                self.hide()
                m.show()
        else:
            QMessageBox.information(self, "提示", "请选择您的身份！")

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

class New_pw(QMainWindow,Ui_mainWindow_pw):
    def __init__(self):
        super(New_pw, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn_connect()

    def btn_connect(self):
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)

    def btn_register(self):
        if self.lineEdit_2.text() != self.lineEdit_3.text():
            QMessageBox.information(self, "提示", "两次密码输入不一致！")
        else:
            pw = self.lineEdit_2.text()
            self.conn = psycopg2.connect(dbname="postgres",
                                             user="zsh",
                                             password="zsh@1234",
                                             host="192.168.56.101",
                                             port="26000")
            self.cur = self.conn.cursor()
            self.cur.execute(f"update student set spassword='{pw}' where spassword='{self.lineEdit.text()}'")
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "修改成功！")
            self.close()


    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

class Register(QMainWindow,Ui_mainWindow_reg):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn_connect()

    def btn_connect(self):
        self.pushButton_2.clicked.connect(self.btn_register)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)

    def btn_register(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        email = self.lineEdit_3.text()
        if len(self.lineEdit.text())==0 or len(self.lineEdit_2.text())==0 or len(self.lineEdit_3.text())==0 :
            QMessageBox.information(self, "提示", "注册信息请全部填写！")
        if self.radioButton.isChecked() == True:
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            self.cur.execute(f"select username from student where username='{username}'")
            new_username = self.cur.fetchone()
            if username == new_username[0]:
                QMessageBox.information(self, "提示", "用户名已被注册！")
            else:
                self.cur.execute('select * from student')
                self.total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
                self.row = self.cur.rowcount
                self.cur.execute(f"insert into student values('{self.row+1}','{username}','{password}','{email}','男');")
                self.conn.commit()
                self.cur.close()
                self.conn.close()
                QMessageBox.information(self, "提示", "注册成功！")
                self.close()
                w.show()
        elif self.radioButton_2.isChecked() == True:
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            self.cur.execute(f"select username from student where username='{username}'")
            new_username = self.cur.fetchone()
            if username == new_username[0]:
                QMessageBox.information(self, "提示", "用户名已被注册！")
            else:
                self.total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
                self.row = self.cur.rowcount
                self.cur.execute(f"insert into student values('{self.row + 1}','{username}','{password}','{email}','女');")
                self.cur.commit()
                self.cur.close()
                self.conn.close()
                QMessageBox.information(self, "提示", "注册成功！")
                self.close()
                w.show()


    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

class Subject(QMainWindow,Ui_mainWindow_sub):
    signal = pyqtSignal(str)  # 定义信号
    def __init__(self):
        super(Subject, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn_connect()

    def btn_connect(self):
        self.pushButton.clicked.connect(self.btn_quiz_p)
        self.pushButton_2.clicked.connect(self.btn_quiz_m)
        self.pushButton_4.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)

    def btn_quiz_p(self):
        self.hide()
        self.signal.emit("python")
        quiz.show()


    def btn_quiz_m(self):
        self.hide()
        self.signal.emit("math")
        quiz.show()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

class Quiz(QMainWindow,Ui_mainWindow_quiz):
    def __init__(self):
        super(Quiz, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.i = -1
        self.answer = [None]*10
        self.btn_connect()
        self.conn()
        self.timez()

    def timez(self):
        self.lcdNumber.setDigitCount(10)
        self.lcdNumber.setMode(QLCDNumber.Dec)
        self.starttime = QDateTime.currentMSecsSinceEpoch()+60 * 60 * 1000
        time = QTimer(self)
        time.setInterval(1000)
        time.timeout.connect(self.refresh)
        time.start()

    def refresh(self):
        startDate = QDateTime.currentMSecsSinceEpoch()
        interval = self.starttime - startDate
        if interval > 0:
            hour = interval // (60 * 60 * 1000)
            min = (interval - hour * 60 * 60 * 1000) // (60 * 1000)
            sec = (interval - hour * 60 * 60 * 1000 - min * 60 * 1000) // 1000
            intervals = str(hour) + ':' + str(min) + ':' + str(sec)
            self.lcdNumber.display(intervals)
        else:
            self.over()
            self.close()

    def conn(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                user="zsh",
                                password="zsh@1234",
                                host="192.168.56.101",
                                port="26000")
        print('successfully connect')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from tab')  # 将数据从数据库中拿出来
        self.total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
        print(self.total)
        self.row = self.cur.rowcount  # 取得记录个数，用于设置表格的行数
        self.vol = len(self.total[0])  # 取得字段数，用于设置表格的列数

        self.label.setText(str(self.total[self.i][0]))
        self.radioButton.setText(str(self.total[self.i][1]))
        self.radioButton_2.setText(str(self.total[self.i][2]))
        self.radioButton_3.setText(str(self.total[self.i][3]))
        self.radioButton_4.setText(str(self.total[self.i][4]))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def mess(self,a):
        # if a == 'python':
            # QMessageBox.information(self,"Q","python")
        # elif a == 'math':
            # QMessageBox.information(self, "Q", "math")
        pass

    def btn_connect(self):
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.over)
        self.pushButton_4.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)

    def back(self):
        self.i -= 1
        if self.radioButton.isChecked() == True:
            self.radioButton.setAutoExclusive(False)
            self.radioButton.setChecked(False)
            self.radioButton.setAutoExclusive(True)
        elif self.radioButton_2.isChecked() == True:
            self.radioButton_2.setAutoExclusive(False)
            self.radioButton_2.setChecked(False)
            self.radioButton_2.setAutoExclusive(True)
        elif self.radioButton_3.isChecked() == True:
            self.radioButton_3.setAutoExclusive(False)
            self.radioButton_3.setChecked(False)
            self.radioButton_3.setAutoExclusive(True)
        elif self.radioButton_4.isChecked() == True:
            self.radioButton_4.setAutoExclusive(False)
            self.radioButton_4.setChecked(False)
            self.radioButton_4.setAutoExclusive(True)

        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        print('successfully connect')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from tab')  # 将数据从数据库中拿出来
        self.total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
        print(self.total)
        self.row = self.cur.rowcount  # 取得记录个数，用于设置表格的行数
        self.vol = len(self.total[0])  # 取得字段数，用于设置表格的列数

        self.label.setText(str(self.total[self.i][0]))
        self.radioButton.setText(str(self.total[self.i][1]))
        self.radioButton_2.setText(str(self.total[self.i][2]))
        self.radioButton_3.setText(str(self.total[self.i][3]))
        self.radioButton_4.setText(str(self.total[self.i][4]))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def next(self):
        self.i += 1
        if self.radioButton.isChecked() == True:
            self.answer[self.i] = 'A'
            self.radioButton.setAutoExclusive(False)
            self.radioButton.setChecked(False)
            self.radioButton.setAutoExclusive(True)
        elif self.radioButton_2.isChecked() == True:
            self.answer[self.i] = 'B'
            self.radioButton_2.setAutoExclusive(False)
            self.radioButton_2.setChecked(False)
            self.radioButton_2.setAutoExclusive(True)
        elif self.radioButton_3.isChecked() == True:
            self.answer[self.i] = 'C'
            self.radioButton_3.setAutoExclusive(False)
            self.radioButton_3.setChecked(False)
            self.radioButton_3.setAutoExclusive(True)
        elif self.radioButton_4.isChecked() == True:
            self.answer[self.i] = 'D'
            self.radioButton_4.setAutoExclusive(False)
            self.radioButton_4.setChecked(False)
            self.radioButton_4.setAutoExclusive(True)

        if (self.i) == len(self.total):
            QMessageBox.information(self,"提示","已经是最后一题了呢！")
            return

        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        print('successfully connect')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from tab')  # 将数据从数据库中拿出来
        total = self.cur.fetchall()  # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
        print(total)
        self.row = self.cur.rowcount  # 取得记录个数，用于设置表格的行数
        self.vol = len(total[0])  # 取得字段数，用于设置表格的列数

        self.label.setText(str(total[self.i][0]))
        self.radioButton.setText(str(total[self.i][1]))
        self.radioButton_2.setText(str(total[self.i][2]))
        self.radioButton_3.setText(str(total[self.i][3]))
        self.radioButton_4.setText(str(total[self.i][4]))
        self.cur.close()
        self.conn.close()

    def over(self):
        '''未完成，须连接数据库'''
        print(self.answer)
        # sub.show()
        # self.hide()


    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

class Manage(QMainWindow,Ui_mainWindow_m):
    def __init__(self):
        super(Manage, self).__init__()
        self.setupUi(self)
        self.sysIcon = QIcon('star.ico')
        self.setWindowIcon(self.sysIcon)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn_connect()

    def btn_connect(self):
        self.pushButton.clicked.connect(self.btn_s_update)
        self.pushButton_2.clicked.connect(self.btn_s_delete)
        self.pushButton_4.clicked.connect(self.btn_m_add)
        self.pushButton_5.clicked.connect(self.btn_q_add)
        self.pushButton_6.clicked.connect(self.btn_q_delete)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.showMinimized)

    def btn_s_update(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, "提示", "用户名为必填项！")
        else:
            if len(self.lineEdit_2.text()) != 0:
                self.cur.execute(f"update student set spassword='{self.lineEdit_2.text()}' where susername='{self.lineEdit.text()}'")
                self.conn.commit()
            if len(self.lineEdit_3.text()) != 0:
                self.cur.execute(f"update student set semail='{self.lineEdit_3.text()}' where susername='{self.lineEdit.text()}'")
                self.conn.commit()
            if len(self.lineEdit_5.text()) != 0:
                self.cur.execute(f"update student set ssex='{self.lineEdit_5.text()}' where susername='{self.lineEdit.text()}'")
                self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "修改成功！")


    def btn_s_delete(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, "提示", "用户名为必填项！")
        else:

            self.cur.execute(
                f"delete from student where susername='{self.lineEdit.text()}'")
            self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "删除成功！")

    def btn_m_add(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.lineEdit_6.text()) == 0:
            QMessageBox.information(self, "提示", "用户名为必填项！")
        else:

            self.cur.execute(f"select * from student where susername='{self.lineEdit_6.text()}'")
            total = self.cur.fetchall()

            self.cur.execute(f"select * from student")
            total_student = self.cur.fetchall()

            self.cur.execute(
                f"insert into teacher values('{len(total_student) + 1}','{total[1]}','{total[2]}','{total[3]}','{total[4]}',)")
            self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "权限赋予成功！")

    def btn_q_add(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.textEdit.text()) == 0 or len(self.textEdit_6.text()) == 0:
            QMessageBox.information(self, "提示", "题目和答案为必填项！")

        else:
            if len(self.textEdit_2.text()) != 0 or len(self.textEdit_3.text()) != 0 \
                    or len(self.textEdit_4.text()) != 0 or len(self.textEdit_5.text()) != 0:
                self.cur.execute(
                    f"insert into question_bank values('{self.textEdit.text()}',"
                    f"'{self.textEdit_2.text()}','{self.textEdit_3.text()}',"
                    f"'{self.textEdit_4.text()}','{self.textEdit_5.text()}','{self.textEdit_6.text()}')")
                self.conn.commit()


            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "添加成功！")

    def btn_q_delete(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.textEdit.text()) == 0 :
            QMessageBox.information(self, "提示", "题目为必填项！")

        else:
            if len(self.textEdit_2.text()) != 0 or len(self.textEdit_3.text()) != 0 \
                    or len(self.textEdit_4.text()) != 0 or len(self.textEdit_5.text()) != 0:
                self.cur.execute(
                    f"delete from question_bank where qname='{self.textEdit.text()}'")
                self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "提示", "删除成功！")

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Student()
    npw = New_pw()
    regist = Register()
    sub = Subject()
    quiz = Quiz()
    m = Manage()
    w.show()
    sys.exit(app.exec_())