#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : wtedt.py
 @Time     : 2022/12/10 21:32
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os,json

from bs4 import BeautifulSoup

f=open('text.html', 'r', encoding='utf-8')
text_list = f.read()
final = []  # 初始化一个列表保存数据

bs=BeautifulSoup(text_list, 'html.parser')
body = bs.body
data = body.find('div', {'id': '7d'})  # 找到div标签且id = 7d
# 下面爬取当天的数据
data2 = body.find_all('div', {'class': 'left-div'})
text = data2[2].find('script').string
text = text[text.index('=') + 1:-2]  # 移除改var data=将其变为json数据
jd = json.loads(text)
dayone = jd['od']['od2']  # 找到当天的数据
final_day = []  # 存放当天的数据
count = 0
for i in dayone:
    temp = []
    if count >= 23:
        temp.append(i['od21'])  # 添加时间
        temp.append(i['od22'])  # 添加当前时刻温度
        temp.append(i['od24'])  # 添加当前时刻风力方向
        temp.append(i['od25'])  # 添加当前时刻风级
        temp.append(i['od26'])  # 添加当前时刻降水量
        temp.append(i['od27'])  # 添加当前时刻相对湿度
        temp.append(i['od28'])  # 添加当前时刻控制质量
        # print(temp)
        final_day.append(temp)
    count = count + 1
# 下面爬取7天的数据
ul = data.find('ul')  # 找到所有的ul标签
li = ul.find_all('li')  # 找到左右的li标签
i = 0  # 控制爬取的天数
for day in li:  # 遍历找到的每一个li
    if i > 0 and i < 7:
        temp = []  # 临时存放每天的数据
        date = day.find('h1').string  # 得到日期
        date = date[0:date.index('日')]  # 取出日期号
        temp.append(date)
        inf = day.find_all('p')  # 找出li下面的p标签,提取第一个p标签的值，即天气
        temp.append(inf[0].string)

        tem_low = inf[1].find('i').string  # 找到最低气温

        if inf[1].find('span') is None:  # 天气预报可能没有最高气温
            tem_high = None
        else:
            tem_high = inf[1].find('span').string  # 找到最高气温
        temp.append(tem_low[:-1])
        if tem_high[-1] == '℃':
            temp.append(tem_high[:-1])
        else:
            temp.append(tem_high)

        wind = inf[2].find_all('span')  # 找到风向
        for j in wind:
            temp.append(j['title'])

        wind_scale = inf[2].find('i').string  # 找到风级
        index1 = wind_scale.index('级')
        temp.append(int(wind_scale[index1 - 1:index1]))
        final.append(temp)
    i = i + 1
print(final)