# -*- coding: utf-8 -*-
import imp
import os.path
import time
import sys
import configparser
import pyautogui
import random
from hashlib import md5
import http
import json
import requests
import keyboard
from aip import AipOcr
from translate import Translator

def printwillkyu():
    print("选定区域实时翻译软件  by willkyu")
    print('============================')
    print("翻译运行中按 Enter 翻译当前选区")
    print('')


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def baiduTranslate(text, appid, appkey):

 
    # 英文->中文 由英文翻译成中文
    from_lang = 'en'
    to_lang = 'zh'
    endpoint = 'http://api.fanyi.baidu.com'  # 固定内容,百度翻译开发者平台
    path = '/api/trans/vip/translate'  # 固定格式 
    url = endpoint + path  # 拼接, 拼接后是网站的api接口(也是个网址,最好自行访问下感受感受)
 
    salt = random.randint(32768, 65536) # 默认,官方要求的必填值
    sign = make_md5(appid + text + str(salt) + appkey) # 同上
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': text, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
 
    # Send request  发送请求获取数据
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()  # 解析获得的 json 数据
 
    # print(result)  # 查看网页返回的内容 (json 解码后的) 
 
    # print(result['trans_result'][0]['dst'])
    # 输出文字第一部分的翻译结果 (以 \n 划分部分) 'dst':翻译结果  'src':原文
 
    # print(json.dumps(result, indent=4, ensure_ascii=  False))
    # 输出的是经过整理的 解码后的结果(建议打印一下查看一下效果)
 
    # print('翻译完毕')
    # 我是要在别的文件调用因此返回一个值,你也可以不返回,直接打印
    # print('原文:\n',result['trans_result'][0]['dst'])
    # print('译文:\n',result['trans_result'][0]['src'])
    # 如果翻译的内容中有 '\n' 请使用循环或者别的方式获取合并后打印,因为会分别翻译,分别储存
    # 这里只读取  [0] 第一个, 默认只翻译一段,因为我的用途是翻译简短的英文单词
 
    return result['trans_result'][0]['dst']



def to_CN(str):
# 翻译中文
    url = 'http://fanyi.youdao.com/translate'
    data = {
        "i": str,  # 待翻译的字符串
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "16081210430989",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }
    res = requests.post(url, data=data).json()
    return res['translateResult'][0][0]['tgt']

def translation():
    """
    识别保存后的图片中的文字
    {'words_result': [{'words': 'message client.basicGeneral(img)'}], 'words_result_num': 1, 'log_id': 1533304524902107597}
    {'words_result': [{'words': 'INFO:Copying 0 resources to EXE'}, {'words': 'INFO:Embedding mani fest i'}, {'words': 'in EXE'}], 'words_result_num': 3, 'log_id': 1533335211894923057}
    :return: 识别后的文字
    """
    i = open(os.path.dirname(os.path.realpath(sys.executable)) + "temp.png", 'rb')
    img = i.read()
    message = client.basicGeneral(img)
    #print(message)
    # message = client.basicAccurate(img)
    if message['words_result']:
        message_len = len(message['words_result'])
        res = ''
        for i in range(message_len):
            res += message['words_result'][i]['words']
            res += ' '
        #print(res)
        return res
    else:
        print("截图区域无文字信息")
        return ''


def deleteimg():
    """
    删除项目目录下的截图
    :return:
    """
    name = os.path.dirname(os.path.realpath(sys.executable)) + "temp.png"
    if os.path.exists(name):
        os.remove(name)


def get_mouse_position(container):
    print('将鼠标移动至翻译区域左上角后按下按键 Q')
    print('将鼠标移动至翻译区域右下角后按下按键 W')
    print('完成后按下按键 S')

    while True:
        
        if keyboard.is_pressed("Q"):
            container = []
            container.insert(0, list(pyautogui.position()))
            time.sleep(0.5)
            print("左上角记录成功", container[0])

        
        if keyboard.is_pressed("W") and len(container) > 0:
            container.insert(1, list(pyautogui.position()))
            container = container[:2]
            time.sleep(0.5)
            print("右下角记录成功", container[1])
            if container[0][0] >= container[1][0] or container[0][1] >= container[1][1]:
                container = []
                print("选定区域不合法，请重新选定")
    
        
        if len(container) == 2 and keyboard.is_pressed("S"):
            print("选定区域完成：",container)
            return container


if __name__ == "__main__":
    printwillkyu()
    container = []
    #sleeptime = eval(input('输入识别间隔(1~3左右): '))

    con = configparser.ConfigParser()
    con.read(os.path.dirname(os.path.realpath(sys.executable)) + "/account.ini", encoding='utf-8')
    APP_ID = con.get("account", "APP_ID")
    API_KEY = con.get("account", "API_KEY")
    SECRECT_KEY = con.get("account", "SECRECT_KEY")
  # Set your own appid/appkey.  设置您自己的appid/appkey。
    appid = con.get("translation", "APP_ID")
    appkey = con.get("translation", "API_KEY")
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    container = get_mouse_position(container)
    print('============================')

    while True:
        #print(1)
        pyautogui.screenshot(os.path.dirname(os.path.realpath(sys.executable)) + "temp.png", region=(container[0][0], container[0][1], container[1][0]-container[0][0], container[1][1]-container[0][1]))
        
        #print(2)
        ocr_res = str(translation())

        #print(3)
        deleteimg()

        if ocr_res == '':
            time.sleep(0.8)
            continue

        #print((4))
        stop = input()
            
        res = baiduTranslate(ocr_res,appid,appkey)
        
        print(ocr_res)
        print(res)
        print('============================')

        #if keyboard.is_pressed("P"):
        #    stop = input('按下回车继续...')
        #else:
        #    time.sleep(sleeptime)

        #if len(container) == 2 and keyboard.is_pressed("esc"):
        #    container = []
        #    print("重新选定区域")
        #    get_mouse_position()


        
        
