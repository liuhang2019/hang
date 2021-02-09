from selenium import webdriver
from time import sleep
import random
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import pymysql

#无可视化
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])

#规避检测
wd = webdriver.Chrome(executable_path='D:/Apycharm/pachong/chromedriver/chromedriver.exe',chrome_options=chrome_options,options=option)

#打开b站
wd.get('https://www.bilibili.com/read/home?spm_id_from=333.851.b_7072696d617279467269656e64736869704c696e6b.1')

#循环 下拉
for i in range(1,4):
    #获取源码数据
    page_text = wd.page_source
    #解析数据
    tree = etree.HTML(page_text)
    titles = tree.xpath('//span[@class="article-title"]/text()')
    for title in titles:
        # =============增加语句===============================
        # 连接数据库
        # ku = input("请输入要操作的库：")
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='20191007lh', database='bilibili',charset='utf8')
        # 生成游标对象
        cur = conn.cursor()
        sql1 = "INSERT INTO bili VALUES (%s)"
        data = [title]
        # ===================================================
        try:
            cur.execute(sql1, data)  # 执行插入的sql语句
            conn.commit()  # 提交到数据库执行
            print("执行成功！")
        except Exception:
            # 发生错误时回滚
            conn.rollback()
            print("出现错误/可能与重复的值有关")
        conn.close()  # 关闭数据库连接

    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)

    print("以将第%s页存入数据库中" % i)

    i += 1

wd.quit()