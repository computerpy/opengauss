#-*-coding:gb2312-*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import string

# ���� SMTP ����
smtp = smtplib.SMTP()
# ���ӣ�connect��ָ��������
smtp.connect("smtp.126.com", port=25)
# ��¼����Ҫ����¼�������Ȩ��
smtp.login(user="python_zsh@126.com", password="WBPWOWBLWIUJZRLN")
pw = random.sample(string.ascii_letters + string.digits, 9)
a = 'z'
for i in pw:
    a += i
# ����MIMEText���󣬲���Ϊ�����ģ�MIME��subtype�����뷽ʽ
message = MIMEText(f'��ʼ�����룺{a}', 'plain', 'utf-8')
message['From'] = Header("z")  # �����˵��ǳ�
message['To'] = Header("your")  # �ռ��˵��ǳ�
message['Subject'] = Header('���߿���ϵͳ�޸�����', 'utf-8')  # ������������
print(message)

smtp.sendmail(from_addr="python_zsh@126.com", to_addrs="zhuoshihao@163.com", msg=message.as_string())
