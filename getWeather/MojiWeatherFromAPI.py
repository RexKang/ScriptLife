#!/bin/env python
# -*- coding=utf-8 -*-

__author__ = u'Rex Kang'
__description__ = u'根据需求，调用墨迹API生成一句话简介。'
__license__ = u'GPL - http://www.fsf.org/licenses/gpl.txt';
__history__ = {
    u'1.0': [u'2017/05/19', u'调用墨迹API，完成基本功能。'],
    u'1.1': [u'2017/06/08', u'增加图标，'],
    u'1.2': [u'2018/09/19', u'获取白天天气替代实况天气，增加图标。'],
    u'1.3': [u'2018/09/27', u'修正没有对应天气图标报错的问题。']
}
import urllib, urllib2, sys, json


def mojiAPI(apiDict, cityID, appCode):
    method = 'POST'
    querys = ''
    bodys = {}
    url = apiDict['host'] + apiDict['path']

    # CityID来自于https://github.com/IceblueSakura/GetWeather/blob/master/Cityid.xml
    bodys['cityId'] = cityID
    bodys['token'] = apiDict['token']
    post_data = urllib.urlencode(bodys)
    request = urllib2.Request(url, post_data)
    request.add_header('Authorization', 'APPCODE ' + appCode)
    # 根据API的要求，定义相对应的Content-Type
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()

    if (content):
        contentDict = {}
        try:
            contentDict = json.loads(content)
        except Exception, err:
            pass
        finally:
            return contentDict

def getCityID(city=u'海口市'):
    cities = {
        u'海口市': '1020',
        u'三亚市': '1022',
        u'乌鲁木齐市': '2505',
        u'西安市': '2182',
    }
    return cities.get(city, '海口市')

# v1.1 Modified Start
def getWetaherIcon(w=u'晴'):
    weatherIcon = {
        u'晴': u'☀️',
        u'阴': u'☁️',
        u'多云': u'⛅',
        u'阵雨': u'🌦',
        u'雨': u'🌧',
        # v1.3 Modified
        u'雷阵雨': u'🌦',
        u'中雨': u'⛈',
        u'大雨': u'⛈',
        u'暴雨': u'⛈'
    }
    # v1.3 Modified
    return weatherIcon.get(w, u'☁️')

def getAOIIcon(aqi=40):
    icon = u'🌱'
    if int(aqi) > 150:
        icon = u'🍂'
    elif int(aqi) > 75:
        icon =  u'🍃'
    return icon
# v1.1 Modified end

def main():
    API = {
        'BriefForecast': {
            'name': u'精简预报3天',
            'host': 'http://freecityid.market.alicloudapi.com',
            'path': '/whapi/json/alicityweather/briefforecast3days',
            'token': '677282c2f1b3d718152c4e25ed434bc4'
        },
        'BriefCondition': {
            'name': u'精简预报实况',
            'host': 'http://freecityid.market.alicloudapi.com',
            'path': '/whapi/json/alicityweather/briefcondition',
            'token': '46e13b7aab9bb77ee3358c3b672a2ae4'
        },
        'AQI': {
            'name': u'精简AQI',
            'host': 'http://freecityid.market.alicloudapi.com',
            'path': '/whapi/json/alicityweather/briefaqi',
            'token': '4dc41ae4c14189b47b2dc00c85b9d124'
        }
    }

    city = u'海口市'
    appCode = '86a53c38ddb546878deab2f87f106e7c'
    strList = [''] * 8
    try:
        resultOfCondition = mojiAPI(API['BriefCondition'], getCityID(city), appCode)
        resultOfForecast = mojiAPI(API['BriefForecast'], getCityID(city), appCode)
        resultOfAQI = mojiAPI(API['AQI'], getCityID(city), appCode)
        
        if resultOfCondition and 'data' in resultOfCondition:
            cond = resultOfCondition['data']['condition']
            # v1.2 Deleted
            # strList[0] = getWetaherIcon(cond['condition'])
            strList[5] = cond['humidity']

        if resultOfForecast and 'data' in resultOfForecast:
            fore = resultOfForecast['data']['forecast'][0]
            # v1.2 Modified
            strList[0] = getWetaherIcon(fore['conditionDay'])
            strList[1] = fore['tempNight']
            strList[2] = fore['tempDay']
            strList[3] = fore['windDirDay']
            strList[4] = fore['windLevelDay']

        if resultOfAQI and 'data' in resultOfAQI:
            strList[7] = resultOfAQI['data']['aqi']['value']
            strList[6] = getAOIIcon(strList[7]) # v1.1 Modified
    except Exception, err:
        # print err
        pass

    finally:
        if len(set(strList)) > 4:
            # v1.2 Modified
            str = u'%s，%s ~ %s℃，🌪%s%s级，💧%s%%，%s%s' % tuple(strList)
            print str.encode('utf-8')
            sys.exit(0)
        else:
            sys.exit(1)


main()
