# -*- coding: utf-8 -*-
import json
import os
from urllib import request
from aip import AipOcr
from flask import Flask, Response
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
IMG_STORE = "/Users/zhikuncheng/Documents/IMG_STORE/"
""" 你的 APPID AK SK """
APP_ID = '11293420'
API_KEY = 'kRdCPbCKskPgtNy7upj420lp'
SECRET_KEY = 'yepRFx7FyNCiQUp18wDawepNU6Dclf0g'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/channel/<channel_name>')
def show_channel_image(channel_name):
    file_name_png = IMG_STORE + "/channel/" + channel_name + ".png"
    file_name_jpg = IMG_STORE + "/channel/" + channel_name + ".jpg"
    file_unknown_png = IMG_STORE + "/channel/" + "TV.png"

    if os.path.exists(file_name_jpg):
        image = open(file_name_jpg, 'r')
        return Response(image, mimetype="image/jpeg")
    if os.path.exists(file_name_png):
        image = open(file_name_png, 'r')
        return Response(image, mimetype="image/jpeg")
    image = open(file_unknown_png, 'r')
    return Response(image, mimetype="image/jpeg")


# OCR识别
@app.route('/image/<image_file>')
def orc_image(image_file):
    """ 你的 APPID AK SK """
    APP_ID = '11293420'
    API_KEY = 'kRdCPbCKskPgtNy7upj420lp'
    SECRET_KEY = 'yepRFx7FyNCiQUp18wDawepNU6Dclf0g'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # options = {}
    # options["language_type"] = "ENG"
    try:
        image = get_file_content(IMG_STORE + image_file)
    except Exception as e:
        return Response(e)
    """ 调用通用文字识别, 图片参数为本地图片 """
    result = client.basicGeneral(image)

    return Response(json.dumps(result, ensure_ascii=False))


@app.route('/tv/<tvname>')
def show_tv_image(tvname):
    # show the tv image for  TV
    # 访问豆瓣根据剧名进行搜索
    target = 'https://www.douban.com/search?cat=1002&q=' + tvname
    html = requests.get(target).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    # 截取封面图片链接
    image_link = soup.find('div', class_='search-result').find('div', class_='result-list'). \
        find('div', class_='result').find('img').get('src')
    filename = image_link.split('/')[-1]
    path_to_img = IMG_STORE + filename
    # 如果曾经下载过图片就从本地获取，否则下载图片并保存
    if not os.path.exists(path_to_img):
        save_img(image_link, filename)
    image = open(IMG_STORE + filename, 'rb').read()
    # 返回图片结果
    resp = Response(image, mimetype="image/jpeg")
    return resp


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def save_img(url, filename):
    try:
        request.urlretrieve(url, filename=IMG_STORE + filename)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
