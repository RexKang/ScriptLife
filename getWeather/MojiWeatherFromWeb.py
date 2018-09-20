#!/bin/env python
# -*- coding=utf-8 -*-

__author__ = u'Rex Kang'
__description__ = u'根据需求，从墨迹Web页面上生成一句话简介。'
__license__ = u'GPL - http://www.fsf.org/licenses/gpl.txt';
__history__ = {
    u'1.0': [u'2018/09/19', u'分析Web页面，获取关键信息，实现基本功能'],
}
import urllib2, sys, re


def getMojiWeb(city=None):
    content=None
    city_url = getCityID(city)
    _url = "https://tianqi.moji.com/weather/china/" + city_url
    try:
        page = urllib2.urlopen(_url)
        content = page.read()
        # print(content)
    except Exception, err:
        print err
    finally:
        return content
    

def getCityID(city=u'海口市'):
    cities = {
        u'海口市': 'hainan/haikou',
        u'三亚市': 'hainan/sanya',
        u'乌鲁木齐市': 'xinjiang/urumqi',
        u'西安市': 'shaanxi/xian',
    }
    return cities.get(city, 'hainan/haikou')


def getWetaherIcon(w=u'晴'):
    weatherIcon = {
        u'晴': u'☀️',
        u'阴': u'☁️',
        u'多云': u'⛅',
        u'阵雨': u'🌦',
        u'雨': u'🌧',
        u'雷阵雨': u'⛈',
        u'中雨': u'🌨',
        u'大雨': u'🌨',
        u'暴雨': u'🌨'
    }
    return weatherIcon.get(w, '阴')

def getAOIIcon(aqi=40):
    icon = u'🌱'
    if int(aqi) > 150:
        icon = u'🍂'
    elif int(aqi) > 75:
        icon =  u'🍃'
    return icon
# v1.1 Modified end

def main():
    hum_regex = u'湿度：(?P<hum>\d+)%'
    weather_regex = u'今天<\/a>\s+<\/li>\s+<li>[\s\S]{100,200}<\/span>\s+' + \
        u'(?P<weather>[^\s]+)\s+<\/li>\s+<li>(?P<t1>\d+).\s.\s(?P<t2>\d+)' + \
        u'[\s\S]{10,100}<em>(?P<wind>.+)<\/em>\s+<b>' + \
        u'(?P<wind_level>[\d-]+).<\/b>[\s\S]{20,100}>\s+(?P<aqi>\d+)\s.\s+<\/strong'
    # print weather_regex
    city = u'海口市'
    strList = [''] * 8
    content = getMojiWeb(city).decode('utf-8')
    try:
        if not content or len(content) < 10240:
            print("Content length error.")
            sys.exit(1)
        hum_result = re.search(hum_regex, content)
        
        if not hum_result:
            print("Hum info error.")
            sys.exit(1)

        weather_result = re.search(weather_regex, content)
        
        if not weather_result:
            print("Weather info error.")
            sys.exit(1)
        
        weather_dict = weather_result.groupdict()
        hum_dict = hum_result.groupdict()
        print("weather: %s" % weather_dict)
        print("hum: %s" % hum_dict)

        strList[0] = getWetaherIcon(weather_dict['weather'])
        strList[1] = weather_dict['t1']
        strList[2] = weather_dict['t2']
        strList[3] = weather_dict['wind']
        strList[4] = weather_dict['wind_level']
        strList[5] = hum_dict['hum']
        strList[7] = weather_dict['aqi']
        strList[6] = getAOIIcon(weather_dict['aqi'])
    except Exception, err:
        print Exception, err
    finally:
        if len(set(strList)) > 4:
            str = u'%s，%s ~ %s℃，🌪%s%s级，💧%s%%，%s%s' % tuple(strList)
            print str.encode('utf-8')
            sys.exit(0)
        else:
            sys.exit(1)

main()
