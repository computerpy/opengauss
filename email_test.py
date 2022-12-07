#-*-coding:gb2312-*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string

# 创建 SMTP 对象
smtp = smtplib.SMTP()
# 连接（connect）指定服务器
smtp.connect("smtp.126.com", port=25)
# 登录，需要：登录邮箱和授权码
smtp.login(user="python_zsh@126.com", password="WBPWOWBLWIUJZRLN")
pw = random.sample(string.ascii_letters + string.digits, 9)
a = 'z'
for i in pw:
    a += i
# 构造MIMEText对象，参数为：正文，MIME的subtype，编码方式
message = MIMEText(f'初始化密码：{a}', 'plain', 'utf-8')
message['From'] = Header("z")  # 发件人的昵称
message['To'] = Header("your")  # 收件人的昵称
message['Subject'] = Header('在线考试系统修改密码', 'utf-8')  # 定义主题内容
print(message)

smtp.sendmail(from_addr="python_zsh@126.com", to_addrs="zhuoshihao@163.com", msg=message.as_string())
