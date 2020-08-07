import datetime
import time
import msvcrt
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

account='###################'
password='###################'
print('请稍后...')
def sendemail(messages):  # 用于签到后发送邮箱提醒
    from_add = '################@qq.com'  # 填写发信方邮箱,邮件从这个邮箱发送到其他的邮箱
    e_password = '#################'  # 此密码是邮箱开启SMTP后的获得的授权码数字
    to_add = '###############@qq.com'  # 填写收信方邮箱
    smtp_server = 'smtp.qq.com'  # 由于使用的是qq邮箱，所以smtp服务器填写qq的服务器
    msg = MIMEText('今日签到情况：' + messages, 'plain', 'GB2312')  # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg['From'] = Header(from_add)  # 括号里的对应发件人邮箱账号
    msg['To'] = Header(to_add, 'GB2312').encode()  # 括号里的对应收件人邮箱账号
    msg['Subject'] = Header('健康打卡情况')  # 邮件的主题
    server = smtplib.SMTP_SSL(smtp_server, 465)  # 发件人邮箱中的SMTP服务器,这里使用的是加密传输，端口是465/587
    server.connect(smtp_server)
    server.login(from_add, e_password)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(from_add, to_add, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
def RGB_to_Hex(rgb):  ###rgb转16进制
        r, g, b = map(int, re.search(
            r'rgb\((\d+),\s*(\d+),\s*(\d+)', rgb).groups())
        rgbstrs = '#'
        rgbstrs += str(hex(r))[-2:].replace('x', '0').upper()
        rgbstrs += str(hex(g))[-2:].replace('x', '0').upper()
        rgbstrs += str(hex(b))[-2:].replace('x', '0').upper()
        return rgbstrs
def daka():
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(r"https://app.nwafu.edu.cn/ncov/wap/default/index")
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[1]/input").send_keys(account)  # 输入账号
    driver.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/input").send_keys(password)  # 输入密码
    driver.find_element_by_class_name("btn").click()  # 点击登陆
    print('正在登陆...')
    time.sleep( 2 )

    driver.find_element_by_xpath("/html/body/div[1]/div/div/section/div[4]/ul/li[6]/div/input").click()  # 获取地理位置
    print('正在获取地理位置...')
    time.sleep( 3 )

    link = driver.find_element_by_xpath("/html/body/div[1]/div/div/section/div[5]/div/a") #获取到gba值
    gbaColor = link.value_of_css_property("background")
    print (gbaColor)

    color = RGB_to_Hex(gbaColor)  # 调用函数获取16进制字符串
    if color == "#4285F4":
        print("今日尚未打卡，即将打卡...")

        driver.find_element_by_xpath("/html/body/div[1]/div/div/section/div[5]/div/a").click()  # 提交信息
        print('正在提交信息...')
        time.sleep(1)

        driver.find_element_by_xpath("//*[@id='wapcf']/div/div[2]/div[2]").click()  # 确认信息
        time.sleep(3)
        message = '打卡成功！打卡时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 打卡成功发送邮件
        sendemail(message)
        print("打卡完成！邮件已发送！程序将在5秒后关闭")
        driver.quit()
    else:
        print("今日已打卡")
        message = '打卡失败！您今日已打卡！请勿重复打卡！'
        sendemail(message)
        print("打卡失败！邮件已发送！程序将在5秒后关闭")
        driver.quit()
def countdown(n):
    while n>=0:
        time.sleep(1)
        print(n)
        n=n-1
    print('运行结束')

daka()
countdown(5)
time.sleep(1)