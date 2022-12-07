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
        # ������ͼ����ʾ��ϵͳ������
        self.trayIcon.show()
        self.setAttribute(Qt.WA_TranslucentBackground)  # ���屳��͸��
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # �����ö����ޱ߿�������������ʾͼ��
        self.setWindowFlags(Qt.FramelessWindowHint)

    # ��������ͼ��
    def createTrayIcon(self):
        aRestore = QAction('�ָ�(&R)', self, triggered=self.showNormal)
        aQuit = QAction('�˳�(&Q)', self, triggered=QApplication.instance().quit)
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
            QMessageBox.information(self, "��ʾ", "�������û�����" )
        else:
            npw.show()
            self.conn = psycopg2.connect(dbname="postgres",
                                         user="zsh",
                                         password="zsh@1234",
                                         host="192.168.56.101",
                                         port="26000")
            self.cur = self.conn.cursor()
            if self.radioButton.isChecked():
                self.cur.execute('select * from student')  # �����ݴ����ݿ����ó���
            else:
                self.cur.execute('select * from teacher')
            self.total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
            self.cur.execute(f"select semail from student where susername='{self.lineEdit.text()}'")
            email = self.cur.fetchone()
            print(email[0])
            # ���� SMTP ����
            smtp = smtplib.SMTP()
            # ���ӣ�connect��ָ��������
            smtp.connect("smtp.126.com", port=25)
            # ��¼����Ҫ����¼�������Ȩ��
            smtp.login(user="python_zsh@126.com", password="WBPWOWBLWIUJZRLN")
            pw_list = random.sample(string.ascii_letters + string.digits, 9)
            pw = 'z'
            for i in pw_list:
                pw += i
            print(pw)
            # ����MIMEText���󣬲���Ϊ�����ģ�MIME��subtype�����뷽ʽ
            message = MIMEText(f'��ʼ�����룺{pw}', 'plain', 'utf-8')
            message['From'] = Header("z")  # �����˵��ǳ�
            message['To'] = Header("your")  # �ռ��˵��ǳ�
            message['Subject'] = Header('���߿���ϵͳ�޸�����', 'utf-8')  # ������������
            smtp.sendmail(from_addr="python_zsh@126.com", to_addrs=f"{email[0]}", msg=message.as_string())
            self.cur.execute(f"update student set spassword='{pw}' where susername='{self.lineEdit.text()}'")
            self.conn.commit()
            self.cur.close()
            self.conn.close()


    def enroll(self):
        if len(self.lineEdit.text())==0 or len(self.lineEdit_2.text())==0  :
            QMessageBox.information(self, "��ʾ", "����д�û��������룡")
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
                QMessageBox.information(self, "��ʾ", "�������")
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
                QMessageBox.information(self, "��ʾ", "�������")
            else:
                self.cur.close()
                self.conn.close()
                self.hide()
                m.show()
        else:
            QMessageBox.information(self, "��ʾ", "��ѡ��������ݣ�")

    # ��д�ƶ��¼�
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
            QMessageBox.information(self, "��ʾ", "�����������벻һ�£�")
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
            QMessageBox.information(self, "��ʾ", "�޸ĳɹ���")
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
            QMessageBox.information(self, "��ʾ", "ע����Ϣ��ȫ����д��")
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
                QMessageBox.information(self, "��ʾ", "�û����ѱ�ע�ᣡ")
            else:
                self.cur.execute('select * from student')
                self.total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
                self.row = self.cur.rowcount
                self.cur.execute(f"insert into student values('{self.row+1}','{username}','{password}','{email}','��');")
                self.conn.commit()
                self.cur.close()
                self.conn.close()
                QMessageBox.information(self, "��ʾ", "ע��ɹ���")
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
                QMessageBox.information(self, "��ʾ", "�û����ѱ�ע�ᣡ")
            else:
                self.total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
                self.row = self.cur.rowcount
                self.cur.execute(f"insert into student values('{self.row + 1}','{username}','{password}','{email}','Ů');")
                self.cur.commit()
                self.cur.close()
                self.conn.close()
                QMessageBox.information(self, "��ʾ", "ע��ɹ���")
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
    signal = pyqtSignal(str)  # �����ź�
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
        self.cur.execute('select * from tab')  # �����ݴ����ݿ����ó���
        self.total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
        print(self.total)
        self.row = self.cur.rowcount  # ȡ�ü�¼�������������ñ�������
        self.vol = len(self.total[0])  # ȡ���ֶ������������ñ�������

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
        self.cur.execute('select * from tab')  # �����ݴ����ݿ����ó���
        self.total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
        print(self.total)
        self.row = self.cur.rowcount  # ȡ�ü�¼�������������ñ�������
        self.vol = len(self.total[0])  # ȡ���ֶ������������ñ�������

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
            QMessageBox.information(self,"��ʾ","�Ѿ������һ�����أ�")
            return

        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        print('successfully connect')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from tab')  # �����ݴ����ݿ����ó���
        total = self.cur.fetchall()  # ��ȡ��ѯ��������, ���Զ�άԪ�����ʽ�洢��, ���Զ�ȡ��Ҫʹ�� data[i][j] �±궨λ
        print(total)
        self.row = self.cur.rowcount  # ȡ�ü�¼�������������ñ�������
        self.vol = len(total[0])  # ȡ���ֶ������������ñ�������

        self.label.setText(str(total[self.i][0]))
        self.radioButton.setText(str(total[self.i][1]))
        self.radioButton_2.setText(str(total[self.i][2]))
        self.radioButton_3.setText(str(total[self.i][3]))
        self.radioButton_4.setText(str(total[self.i][4]))
        self.cur.close()
        self.conn.close()

    def over(self):
        '''δ��ɣ����������ݿ�'''
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
            QMessageBox.information(self, "��ʾ", "�û���Ϊ�����")
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
            QMessageBox.information(self, "��ʾ", "�޸ĳɹ���")


    def btn_s_delete(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, "��ʾ", "�û���Ϊ�����")
        else:

            self.cur.execute(
                f"delete from student where susername='{self.lineEdit.text()}'")
            self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "��ʾ", "ɾ���ɹ���")

    def btn_m_add(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.lineEdit_6.text()) == 0:
            QMessageBox.information(self, "��ʾ", "�û���Ϊ�����")
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
            QMessageBox.information(self, "��ʾ", "Ȩ�޸���ɹ���")

    def btn_q_add(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.textEdit.text()) == 0 or len(self.textEdit_6.text()) == 0:
            QMessageBox.information(self, "��ʾ", "��Ŀ�ʹ�Ϊ�����")

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
            QMessageBox.information(self, "��ʾ", "��ӳɹ���")

    def btn_q_delete(self):
        self.conn = psycopg2.connect(dbname="postgres",
                                     user="zsh",
                                     password="zsh@1234",
                                     host="192.168.56.101",
                                     port="26000")
        self.cur = self.conn.cursor()
        if len(self.textEdit.text()) == 0 :
            QMessageBox.information(self, "��ʾ", "��ĿΪ�����")

        else:
            if len(self.textEdit_2.text()) != 0 or len(self.textEdit_3.text()) != 0 \
                    or len(self.textEdit_4.text()) != 0 or len(self.textEdit_5.text()) != 0:
                self.cur.execute(
                    f"delete from question_bank where qname='{self.textEdit.text()}'")
                self.conn.commit()

            self.cur.close()
            self.conn.close()
            QMessageBox.information(self, "��ʾ", "ɾ���ɹ���")

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