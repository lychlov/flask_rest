# -*- coding: utf-8 -*-
import os
import urllib

from flask import Flask, Response
import requests
from lxml import etree

app = Flask(__name__)
IMG_STORE = "/home/ops/work_space/IMG_STORE/"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/channel/<channel_name>')
def show_channel_image(channel_name):
    file_name_png = IMG_STORE + "/channel/" + channel_name + ".png"
    file_name_jpg = IMG_STORE + "/channel/" + channel_name + ".jpg"
    file_unknown_png = IMG_STORE + "/channel/" + "TV.png"

    if os.path.exists(file_name_jpg):
        image = file(file_name_jpg)
        return Response(image, mimetype="image/jpeg")
    if os.path.exists(file_name_png):
        image = file(file_name_png)
        return Response(image, mimetype="image/jpeg")
    image = file(file_unknown_png)
    return Response(image, mimetype="image/jpeg")


@app.route('/tv/<tvname>')
def show_tv_image(tvname):
    # show the tv image for  TV
    # 访问豆瓣根据剧名进行搜索
    target = 'https://www.douban.com/search?cat=1002&q=' + tvname
    html = requests.get(target).content.decode('utf-8')
    doc_tree = etree.HTML(html)
    # 截取封面图片链接
    image_links = doc_tree.xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[1]/a/img/@src')
    filename = image_links[0].split('/')[-1]
    path_to_img = IMG_STORE + filename
    # 如果曾经下载过图片就从本地获取，否则下载图片并保存
    if not os.path.exists(path_to_img):
        print "New download"
        save_img(image_links[0], filename)
    image = file(IMG_STORE + filename)
    # 返回图片结果
    resp = Response(image, mimetype="image/jpeg")
    return resp


def save_img(url, filename):
    # filename = url[:]
    try:
        urllib.urlretrieve(url, filename=IMG_STORE + filename)
    except IOError as e:
        print '文件操作失败', e
    except Exception as e:
        print '错误 ：', e


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
