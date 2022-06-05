# -*- coding: utf-8 -*-
import imp
import os.path
import time
import sys
import configparser
import pyautogui
import requests
import keyboard
from aip import AipOcr
from translate import Translator

def printwillkyu():
    print("选定区域实时翻译软件  by willkyu")
    print('============================')
    print("翻译运行中长按 P 暂停, 长按 esc 重新选区")
    print('')


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
    i = open(os.path.dirname(os.path.dirname(os.path.realpath(sys.executable))) + "temp.png", 'rb')
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
    name = os.path.dirname(os.path.dirname(os.path.realpath(sys.executable))) + "temp.png"
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
    sleeptime = eval(input('输入识别间隔(1~3左右): '))
    con = configparser.ConfigParser()
    con.read(os.path.dirname(os.path.dirname(os.path.realpath(sys.executable))) + "/account.ini", encoding='utf-8')
    APP_ID = con.get("account", "APP_ID")
    API_KEY = con.get("account", "API_KEY")
    SECRECT_KEY = con.get("account", "SECRECT_KEY")
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    container = get_mouse_position(container)
    print('============================')

    while True:
        #print(1)
        pyautogui.screenshot(os.path.dirname(os.path.dirname(os.path.realpath(sys.executable))) + "temp.png", region=(container[0][0], container[0][1], container[1][0]-container[0][0], container[1][1]-container[0][1]))
        
        #print(2)
        ocr_res = str(translation())

        #print(3)
        deleteimg()

        if ocr_res == '':
            time.sleep(0.8)
            continue

        #print((4))
        res = to_CN(ocr_res)
        
        print(ocr_res)
        print(res)
        print('============================')

        if keyboard.is_pressed("P"):
            stop = input('按下回车继续...')
        else:
            time.sleep(sleeptime)

        if len(container) == 2 and keyboard.is_pressed("esc"):
            container = []
            print("重新选定区域")
            get_mouse_position()


        
        
