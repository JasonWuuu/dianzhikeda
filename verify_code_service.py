import requests
import cv2
import numpy as np
import base64
import random


def get_verify_code_from_yi_yuan(img_base64):
    url = 'http://route.showapi.com/184-5'
    data = {
        'img_base64': img_base64,
        'typeId': 34,
        'convert_to_jpg': 0,
        'needMorePrecise': 1,
        'showapi_appid': '80206',
        'showapi_sign': '63c3fecd530945b4ab2b62290c9f304e'
    }

    with requests.post(url, data=data) as res:
        res = res.json()
        if res['showapi_res_body']['ret_code'] == 0:
            return res['showapi_res_body']['Result']


def get_img_base64(driver):
    url = 'https://www.uestcedu.com/ifree/VerifyUtil.do?' + str(random.random())

    cookies = {
        'JSESSIONID': driver.get_cookie('JSESSIONID')['value']
    }
    with requests.get(url, cookies=cookies) as r:
        return base64.b64encode(r.content)


def get_verify_code(driver):
    img_base64 = get_img_base64(driver)
    return get_verify_code_from_yi_yuan(img_base64)


if __name__ == '__main__':
    # print(cv2.__version__)
    # img = cv2.imread('screen_shoot.png')
    # print(img.shape)
    # cropped=img[0,400]
    # cv2.imwrite('1.png',cropped)

    s = get_img_base64(None, 'https://www.uestcedu.com/ifree/VerifyUtil.do?0.3350180113452019')
    print(s)
