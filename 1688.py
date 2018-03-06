#!/usr/bin/env python
#encoding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
# from http.cookiejar import CookieJar
import http.cookiejar
import time
import urllib
import sys
import os
import re
import csv
import random
import importlib
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

item_name = '水壶'
# 打开一个火狐浏览器
driver = webdriver.Firefox()

# 淘宝登录的url
login_url = 'https://login.taobao.com/member/login.jhtml'
# 淘宝用户名
tb_username = '***'
# 淘宝密码
tb_password = '***'

# 跳转到登录页面
driver.get(login_url)
# 找到登录框右上角的标志，J_Quick2Static是切换到用户名密码登录的界面
quick_2_static = driver.find_element_by_id('J_Quick2Static')
# 如果J_Quick2Static显示了，说明现在是二维码登录界面，点击切换用户名密码登录界面
if quick_2_static.is_displayed():
    quick_2_static.click();
# 等待随机时间，以免被反爬虫
time.sleep(random.uniform(0, 1))
# 找到账号登录框的DOM节点，并且在该节点内输入账号
driver.find_element_by_name('TPL_username').send_keys(tb_username)
# 等待随机时间，以免被反爬虫
time.sleep(random.uniform(1, 2))
# 找到账号密码框的DOM节点，并且在该节点内输入密码
driver.find_element_by_name('TPL_password').send_keys(tb_password)
# 等待随机时间，以免被反爬虫
time.sleep(random.uniform(1, 2))

# 找到登录窗口滑动验证的方块
slider_square = driver.find_element_by_id('nc_1_n1z')

# 判断方块是否显示，是则模拟鼠标滑动，否则跳过
if slider_square.is_displayed():
    # 鼠标点击滑块并保持
    ActionChains(driver).click_and_hold(slider_square).perform()
    # 鼠标多次向右移动随机距离
    for i in range(0,5):
        ActionChains(driver).move_by_offset(random.randint(60,80), 5).perform()
    # 抬起鼠标左键
    ActionChains(driver).release()
    # 等待随机时间，以免被反爬虫
    time.sleep(random.uniform(0, 1))

# 找到账号登录框的提交按钮，并且点击提交
driver.find_element_by_name('TPL_password').send_keys(Keys.ENTER)

# 睡眠5秒，防止未登录就进行了其他操作
time.sleep(10)
#取得cookie
driver.get_cookies()
#cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
#cookiestr = ';'.join(item for item in cookie)
#print(cookie)

url = 'https://s.1688.com/company/company_search.htm?&keywords=' + urllib.quote(item_name)

driver.get(url)

# 新建一个data.csv文件，并且将数据保存到csv中
csvfile = file('data1.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
# 写入标题，
writer.writerow(('企业名称', '主页', '产品', '联系人', '电话', '手机', '传真', '地址', '邮编',))

cnt = 0;
# 总共有100页，使用for循环采集
for page in xrange(1, 2):
    # 捕捉异常
    try:

        # 商户页面的url
        url = 'https://s.1688.com/company/company_search.htm?&keywords=' + urllib.quote(item_name) + '&beginPage=' + str(page)
        print(url)
        # 跳转到商户页面的url
        driver.get(url)
        if '异常' in driver.page_source:
            print('输入网页验证码')
            time.sleep(10)
        # 睡眠3秒，等待转到页面
        else:
            time.sleep(5)


        # 获取企业名称列表
        title = driver.find_elements_by_css_selector("a[class=list-item-title-text]")
        # 获取产品
        product = driver.find_elements_by_xpath("//div[@class=\"detail-float-items\"]")

        title_values = ['']*len(title)
        href_values = ['']*len(title)
        host_values = ['']*len(title)
        product_values = ['']*len(title)
        
        for i in range(len(title)):
            # 获取标题的值
            title_values[i] = title[i].get_attribute('title')
            #print(title_value)
            # 获取跳转的url
            titlehref = title[i].get_attribute('href') 
            proto, rest = urllib.splittype(titlehref)
            host,rest = urllib.splithost(rest)
            host_values[i] = str(proto +'://' + host)
            href_values[i] = str(proto +'://' + host) + '/page/contactinfo.htm'
            #print(href_value)
            #print(href_value)
            # 获取经营范围
            product_values[i] = product[i].text
            
        for i in range(len(title)):
        #for i in range(2):
            print("第",cnt+1,"个商家")
            cnt = cnt + 1
            title_value = title_values[i]
            print(title_value)
            href_value = href_values[i]
            print(href_value)
            #print(href_value)
            # 获取经营范围
            product_value = product_values[i]

#            print(href_value)
            driver.get(href_value)

            html = driver.page_source

            #print(html)
 #           if '网络环境有异常' in html:
 #               print('输入网页验证码')
 #               time.sleep(10)
            #print(html)
            # 进行信息匹配

            soup = BeautifulSoup(html, "html.parser")

            contact_name = soup.find(name = "a", attrs = {"class":"membername"}).string

            print(contact_name)

            info = soup.find(name = "div", attrs = {"class":"contcat-desc"})

            if info == None:
                continue
            
            #print(info)
            
            data = ['','','','','','']
            idx = 0
            for string in info.stripped_strings:
                if idx % 2 == 0:
                    strstr = str(string)
                    if strstr.startswith('电'):
                        flag = 0
                    elif strstr.startswith('移'):
                        flag = 1
                    elif strstr.startswith('传'):
                        flag = 2
                    elif strstr.startswith('地'):
                        flag = 3
                    elif strstr.startswith('邮'):
                        flag = 4
                    elif strstr.startswith('公'):
                        flag = 5
                    else:
                        flag = 6
                else:
                    if flag == 6:
                        continue
                    else:
                        data[flag] = str(string)
                idx = idx + 1

                
            print(data[3])

            # 判断公司主页，一个或者两个
            address1 = host_values[i]
            address2 = data[5]
            address = ''
            if address1 == address2 or len(data[5]) < 2:
                address = address1
            else:
                address = address1 + ', ' + address2

            # 判断电话
            if len(data[0]) <= 4:
                phone = '无'
            else:
                phone = data[0]

            # 判断手机
            if len(data[1]) <= 4:
                telphone = '无'
            else:
                telphone = data[1]

            # 判断传真
            if len(data[2]) <= 4:
                fax = '无'
            else:
                fax = data[2]

            # 判断地址
            if len(data[3]) <= 4:
                data[3] = '无'

            # 判断邮编
            if len(data[4]) <= 4:
                data[4] = '无'

            outdata = (
                title_value,
                address,
                product_value,
                contact_name,
                phone,
                telphone,
                fax,
                data[3],
                data[4],
            )
            #print(outdata)
            writer.writerow(outdata)
	
    except Exception as e:
        print('error')
        print(e)
        continue
# 关闭csv
csvfile.close()
# 关闭模拟浏览器
driver.close()