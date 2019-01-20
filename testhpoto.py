# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 01:36:56 2019

@author: elopsuc
"""
import os
import json
import urllib.request
#基于百度地图API下的经纬度信息来解析地理位置信息
def getlocation(lat,lng):
    #31.809928, 102.537467, 3019.300
    #lat = '31.809928'
    #lng = '102.537467'
    lat=str(lat)
    lng=str(lng)
    url = 'http://api.map.baidu.com/geocoder/v2/?location=' + lat + ',' + lng + '&output=json&pois=1&ak=XgrnXcZpGRgljoxfTiZ19G73xAcKhGyS'
    req = urllib.request.urlopen(url)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    return json.loads(res)

#json序列化解析数据(lat:纬度，lng:经度)
def jsonFormat(lat,lng):
    str = getlocation(lat,lng)
    dictjson={}#声明一个字典
    #get()获取json里面的数据
    jsonResult = str.get('result')
    #print(jsonResult)
    address = jsonResult.get('addressComponent')
    #国家
    country = address.get('country')
    #国家编号（0：中国）
    country_code = address.get('country_code')
    #省
    province = address.get('province')
    #城市
    city = address.get('city')
    #城市等级
    city_level = address.get('city_level')
    #县级
    district = address.get('district')
    street= address.get('street')
    streetNumber= address.get('street_number')
    #把获取到的值，添加到字典里（添加）
    dictjson['country']=country
    dictjson['country_code'] = country_code
    dictjson['province'] = province
    dictjson['city'] = city
    dictjson['city_level'] = city_level
    dictjson['district']=district
    dictjson['street']=street
    dictjson['streetNumber']=streetNumber
    return dictjson

def exifread_infos(photo):
    import exifread 
    #加载 ExifRead 第三方库  https://pypi.org/project/ExifRead/
    #获取照片时间、经纬度信息
    #photo参数：照片文件路径
    
    # Open image file for reading (binary mode) 
    f = open(photo, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        #拍摄时间
        EXIF_Date=tags["EXIF DateTimeOriginal"].printable
        #纬度
        LatRef=tags["GPS GPSLatitudeRef"].printable
        Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
        if LatRef != "N":
            Lat=Lat*(-1)
        #经度
        LonRef=tags["GPS GPSLongitudeRef"].printable
        Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
        if LonRef!="E":
            Lon=Lon*(-1)
        f.close()
    except :
        return "ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return EXIF_Date,Lat,Lon
dirs=(r"C:\Users\ELOPSUC\Desktop\test\New folder")
for file in os.listdir(dirs):
        filename=os.path.splitext(file)                       
        if filename[1] == ".jpg":
             
            photo=dirs+"\\"+file
            x=exifread_infos(photo)
            
            if type(x)!=type("1"):
                #print(file)                
                s=jsonFormat(x[1],x[2])
                print("该照片拍摄地址位于： %s" % s['province'],s['city'],s['street'],s['streetNumber'])
                