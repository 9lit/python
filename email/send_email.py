import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
 
def send_plain_text_email(sender_email, sender_password, recipient_email, subject, body):
    # 创建邮件内容
    message = MIMEMultipart()
    message.attach(MIMEText(body, 'html', 'utf-8'))
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
 
    # 设置SMTP服务器信息
    smtp_server = "smtp.qq.com"
    smtp_port = 587  # 假设使用的是TLS加密，端口号为587
 
    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP(smtp_server, smtp_port); server.starttls()  # 开启TLS加密
 
        # 登录邮箱账号
        server.login(sender_email, sender_password)
 
        # 发送邮件
        server.sendmail(sender_email, [recipient_email], message.as_string())
 
        print("0")
    except Exception as e:
        print("1: ", e)
    finally:
        # 关闭连接
        server.quit()

def format_to_html(old_body):
    # 将普通字符串格式化为 html 
    body_split = old_body.split("\n")
    new_body = ""
    
    for body_line in body_split:
        if "===" in body_line: line = "<h3>{}</h3>".format(body_line)
        
        elif "https://" in body_line: line = "<a href='{}'> webdav 地址 </a>".format(body_line)
        
        else: line = "{}</br>".format(body_line)

        new_body += line

    return new_body

# 获取参数
try:
    params = sys.argv
    # 输入发件人邮箱地址、密码、收件人邮箱地址
    sender_email = params[1]; sender_password = params[2]; recipient_email = params[3]

    # 邮件主题和内容
    title = params[4]
    body=format_to_html(params[5])

except IndexError as e:
    exit(f"1: {e}")

# 发送邮件
send_plain_text_email(sender_email, sender_password, recipient_email, title, body)