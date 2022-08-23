import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
import requests
import math

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)



app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
city = os.environ['CITY']

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day



def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])


#词霸每日一句
def get_ciba():
    if (Whether_Eng!="否"):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en
    else:
        return "",""


#彩虹屁
def caihongpi():
    if (caihongpi_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':caihongpi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/caihongpi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        if("XXX" in data):
            data.replace("XXX","蒋蒋")
        return data
    else:
        return ""

#健康小提示API
def health():
    if (health_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':health_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/healthtip/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        return data
    else:
        return ""

#星座运势
def lucky():
    if (lucky_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lucky_API,'astro':astro})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/star/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = "速配星座："+str(data["newslist"][7]["content"])+"\n爱情指数："+str(data["newslist"][1]["content"])+"   工作指数："+str(data["newslist"][2]["content"])+"\n今日概述："+str(data["newslist"][8]["content"])
        return data
    else:
        return ""

#励志名言
def lizhi():
    if (lizhi_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lizhi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/lzmy/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        return data["newslist"][0]["saying"]
    else:
        return ""
        

#下雨概率和建议
def tip():
    if (tianqi_API!="否"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':tianqi_API,'city':city})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tianqi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        pop = data["newslist"][0]["pop"]
        tips = data["newslist"][0]["tips"]
        return pop,tips
    else:
        return "",""

#推送信息
def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, pipi, lizhi, pop, tips, note_en, note_ch, health_tip, lucky_):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },

            "pipi": {
                "value": pipi,
                "color": get_color()
            },

            "lucky": {
                "value": lucky_,
                "color": get_color()
            },

            "lizhi": {
                "value": lizhi,
                "color": get_color()
            },

            "pop": {
                "value": pop,
                "color": get_color()
            },

            "health": {
                "value": health_tip,
                "color": get_color()
            },

            "tips": {
                "value": tips,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("./config.json", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    
    # 传入省份和市获取天气信息
    weather, temperature, highest, lowest = get_weather()
    data = {"weather":{"value":weather,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"highest": {"value":highest,"color":get_random_color()},"lowest":{"value":lowest, "color":get_random_color()}}
    #获取彩虹屁API
    caihongpi_API=config["caihongpi_API"]
    #获取励志古言API
    lizhi_API=config["lizhi_API"]
    #获取天气预报API
    tianqi_API=config["tianqi_API"]
    #是否启用词霸每日金句
    Whether_Eng=config["Whether_Eng"]
    #获取健康小提示API
    health_API=config["health_API"]
    #获取星座运势API
    lucky_API=config["lucky_API"]
    #获取星座
    astro = config["astro"]
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    #彩虹屁
    pipi = caihongpi()
    #健康小提示
    health_API=config["health_API"]
 
    #下雨概率和建议
    pop,tips = tip()
    #励志名言
    lizhi = lizhi()
    #星座运势
    lucky_ = lucky()
    # 公众号推送消息
    for user_id in user_ids:
        send_message(user_id,  city, weather, highest, lowest, pipi, lizhi,pop,tips, note_en, note_ch, health_API, lucky_ )
    import time
    time_duration = 3.5
    time.sleep(time_duration)
