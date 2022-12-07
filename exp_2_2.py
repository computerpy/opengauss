#-*-coding:gb2312-*-
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtWidgets import QDialog, QFrame, QVBoxLayout, QLineEdit, QGraphicsOpacityEffect, QPushButton, QApplication
import sys

class logindialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('XXXXXXX')
        # self.setWindowIcon(QIcon('wheel.ico'))
        self.resize(1920, 1080)
        # self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('background3.jpg')))
        self.setPalette(palette)

        # 设置界面控件

        self.frame = QFrame(self)
        self.frame.move(800, 300)
        # self.verticalLayout = QVBoxLayout(self.frame)
        self.mainLayout = QVBoxLayout(self.frame)

        # self.nameLb1 = QLabel('&Name', self)
        # self.nameLb1.setFont(QFont('Times', 24))
        self.nameEd1 = QLineEdit(self)
        self.nameEd1.setPlaceholderText("Account")
        self.nameEd1.setFont(QFont('Arial', 24))
        # 设置透明度
        op1 = QGraphicsOpacityEffect()
        op1.setOpacity(0.5)
        self.nameEd1.setGraphicsEffect(op1)
        # 设置文本框为圆角
        self.nameEd1.setStyleSheet('''QLineEdit{border-radius:5px;}''')
        # self.nameLb1.setBuddy(self.nameEd1)

        # self.nameLb2 = QLabel('&Password', self)
        # self.nameLb2.setFont(QFont('Times', 24))
        self.nameEd2 = QLineEdit(self)
        self.nameEd2.setPlaceholderText("Admin")
        self.nameEd2.setFont(QFont('Arial', 24))
        op2 = QGraphicsOpacityEffect()
        op2.setOpacity(0.5)
        self.nameEd2.setGraphicsEffect(op2)
        self.nameEd2.setStyleSheet('''QLineEdit{border-radius:5px;}''')
        # self.nameLb2.setBuddy(self.nameEd2)

        self.nameEd3 = QLineEdit(self)
        self.nameEd3.setPlaceholderText("Password")
        self.nameEd3.setFont(QFont('Arial', 24))
        op5 = QGraphicsOpacityEffect()
        op5.setOpacity(0.5)
        self.nameEd3.setGraphicsEffect(op5)
        self.nameEd3.setStyleSheet('''QLineEdit{border-radius:5px;}''')

        self.btnOK = QPushButton('OK')
        op3 = QGraphicsOpacityEffect()
        op3.setOpacity(0.5)
        self.btnOK.setGraphicsEffect(op3)
        self.btnOK.setStyleSheet(
            '''QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
            QPushButton{font-family:'Arial';color:#FFFFFF;}''')  # font-family中可以设置字体大小，如下font-size:24px;

        self.btnCancel = QPushButton('Cancel')
        op4 = QGraphicsOpacityEffect()
        op4.setOpacity(0.5)
        self.btnCancel.setGraphicsEffect(op4)
        self.btnCancel.setStyleSheet(
            '''QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
            QPushButton{font-family:'Arial';color:#FFFFFF;}''')

        self.btnOK.setFont(QFont('Microsoft YaHei', 24))
        self.btnCancel.setFont(QFont('Microsoft YaHei', 24))

        # self.mainLayout.addWidget(self.nameLb1, 0, 0)
        self.mainLayout.addWidget(self.nameEd1)

        # self.mainLayout.addWidget(self.nameLb2, 1, 0)
        self.mainLayout.addWidget(self.nameEd2)

        self.mainLayout.addWidget(self.nameEd3)

        self.mainLayout.addWidget(self.btnOK)
        self.mainLayout.addWidget(self.btnCancel)

        self.mainLayout.setSpacing(60)

        '''
        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        # self.lineEdit_account.move(900, 540)
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)
        '''

        ###### 绑定按钮事件
        self.btnOK.clicked.connect(self.on_pushButton_enter_clicked)
        self.btnCancel.clicked.connect(QCoreApplication.instance().quit)

    def on_pushButton_enter_clicked(self):
        # 账号判断
        if self.nameEd1.text() == "":
            return

        # 权限判断
        if self.nameEd2.text() == "":
            return

        # 密码判断
        if self.nameEd3.text() == "":
            return

        # 通过验证，关闭对话框并返回1
        self.accept()


if __name__ == "__maim__":
    app = QApplication(sys.argv)
    log = logindialog()
    log.show()
    sys.exit(app.exec_())
