# lab3

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os

CODE = 'utf-8'
mail_server = 'smtp.qq.com'
mail_port = 25
username = '2662765987@qq.com'
password = 'jhrmbqbhstydecjc'
receivers = ['zyzstchhh@163.com']

# 选择一个邮件服务器及其端口号
"""
    邮件类型为"multipart/alternative"的邮件包括纯文本正文（text/plain）
    和超文本正文（text/html）。
    邮件类型为"multipart/related"的邮件正文中包括图片，声音等内嵌资源。
    邮件类型为"multipart/mixed"的邮件包含附件。向上兼容，
    如果一个邮件有纯文本正文，超文本正文，内嵌资源，附件，则选择mixed类型。
"""
message = MIMEMultipart('mixed')
subject = 'SMTP TEST'
message['Subject'] = Header(subject, CODE)
message['From'] = Header(username, CODE)
message['To'] = Header(';'.join(receivers), CODE)

text_file_path = "smtp_test.txt"


# 构造文字内容
def msg_text_attach(plain_text):
    """读取文件或者使用变量传递纯文本"""
    if os.path.isfile(plain_text):
        """如果传递的是路径，则读取文本"""
        with open(plain_text, 'rb') as text_file:
            plain_text = text_file.read()
    msg_text_plain = MIMEText(plain_text, 'plain', 'utf8')
    message.attach(msg_text_plain)


# 构造HTML内容
def html_text_attach(html_text):
    """不需要做替换掉 html构造"""
    html_msg = MIMEText(html_text, 'html', 'utf-8')
    message.attach(html_msg)


def msg_text_html_attach(html_text_file):
    """构造一个需要替换图片的html"""
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)
    try:
        with open(html_text_file, 'r', encoding='utf8') as html_file:
            html_text_content = html_file.read()
    except Exception as eh:
        print('未找到html文件', eh)
    msg_alternative.attach(MIMEText(html_text_content, 'html', 'utf8'))


def add_image(image_path, cid):
    # 指定图片为当前目录
    with open(image_path, 'rb') as image_file:
        msg_image = MIMEImage(image_file.read())

    # 定义图片id，在html文本中引用
    msg_image.add_header('Content-ID', cid)
    message.attach(msg_image)


# 构造图片链接
def image_attach(image_file_path, imgid, filename=None):
    if filename is None:
        """如果不重命名文件，则默认使用源文件名"""
        filename = image_file_path
    try:
        with open(image_file_path, 'rb') as image_file:
            image_content = image_file.read()
    except Exception as ei:
        print('未找到图片文件', ei)
    image = MIMEImage(image_content)
    image.add_header('Content-ID', imgid)   # image1是照片别名，可以在HTML代码中引用
    image['Content-Disposition'] = f'attachment; filename={filename}'
    message.attach(image)


# 构造附件
def send_annex_file(annex_file_path, annex_filename=None):
    """传入附加文件路径和文件名(重命名附件，可以省略，默认为源文件名)"""
    if annex_filename is None:
        annex_filename = annex_file_path
    try:
        with open(annex_file_path, 'rb') as annex_file:
            send_file = annex_file.read()
    except Exception as es:
        print('未找到附件', es)

    text_appendix = MIMEText(send_file, 'base64', 'utf-8')
    text_appendix["Content-Type"] = 'application/octet-stream'
    # 以下附件可以重命名成：核心数据.xlsx
    # text_appendix["Content-Disposition"] = 'attachment; filename="核心数据.xlsx"'
    # 另一种附件重命名实现方式
    text_appendix.add_header('Content-Disposition', 'attachment', filename=annex_filename)
    message.attach(text_appendix)


def sendEmail():
    # html和text纯文本内容不能同时存在，html会覆盖掉text纯文本
    # 构造文字内容
    # msg_text = """
    #             2013747
    #             SMTP TEST
    #             文字，html,图片，附件实现
    #             参考：https://zhuanlan.zhihu.com/p/318387004
    #             """
    #
    # msg_text_attach(msg_text)

    # # 构造HTML内容
    # html_content = """
    #     <html>
    #       <head></head>
    #       <body>
    #          <p>Python 邮件发送测试...<br>
    #            How are you?<br>
    #            Here is the <a href="http://www.zhihu.com/people/4k8k">link</a> you wanted.<br>
    #          </p>
    #       </body>
    #     </html>
    #     """
    # html_text_attach(html_content)

    # 构造HTML内容（带图片）
    # 使用字典保存HTML文件路径
    html_file_path = {
        "html1": "Web.html",
        "html2": "smtp.html"
    }

    image_paths = {
        "image1": "nankai.jpg",
    }

    image_cids = {
        "image1": "nankai",
    }
    msg_text_html_attach(html_file_path.get("html2"))
    add_image(image_paths.get('image1'), image_cids.get('image1'))  # 替换cid1

# 图片
    image_attach('nankai.jpg','南开')

# 构造附件
    annex_path = {
        "file1": "smtp_test.txt",
    }
    send_annex_file(annex_path["file1"])




    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_server, mail_port)  # 25为SMTP端口号
        smtpObj.login(username, password)  # 会返回(状态码, "字符串解释")元组信息
        smtpObj.sendmail(username, receivers, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("Error: 无法发送邮件  | " + str(e))


if __name__ == '__main__':
    sendEmail()
