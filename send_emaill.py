import smtplib, ssl, random

def send_email(receiver):
    host = "smtp.gmail.com"
    port = 465
    username = "littlecoders10@gmail.com"
    password = "ahkb dlqz uubs dxav"

    my_context = ssl.create_default_context()
    code = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
    message = f"""\
Subject: Your code. Thanks For Choosing Us

Your code is:
{code}
"""
    with smtplib.SMTP_SSL(host, port, context=my_context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
        return code
