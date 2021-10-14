# -*- coding: utf-8 -*-

"""
    @Author 坦克手贝塔
    @Date 2021/6/1 14:40
"""
import requests
import base64
import os
import math

FILE_IN_PATH = r'./images/'
FILE_OUT_PATH = r'./images/'
CLIENT_ID = "[百度智能云获取]"
CLIENT_SECRET = "[百度智能云获取]"


# 生成access_token
def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(CLIENT_ID, CLIENT_SECRET)
    my_response = requests.get(host)
    my_access_token = my_response.json()["access_token"]
    return my_access_token


# 获取文件夹中的所有文件
def get_file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


if __name__ == "__main__":
    # 获取文件夹中所有的文件名
    my_files = get_file_name(FILE_IN_PATH)
    for i in range(0, len(my_files)):
        # 判断文件大小，超过10MB不做处理
        file_size = os.stat(FILE_IN_PATH + my_files[i]).st_size
        file_size_MB = math.ceil(file_size / 1024 / 1024)
        if file_size_MB > 10:
            continue
        # 请求地址
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
        # 二进制方式打开图片文件
        f = open(FILE_IN_PATH + my_files[i], 'rb')
        img = base64.b64encode(f.read())
        f.close()
        params = {"image": img}
        access_token = get_access_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        # 获取
        response = requests.post(request_url, data=params, headers=headers)
        img_str = response.json()["image"]
        img_data = base64.b64decode(img_str)
        # 对增强后的文件进行重命名
        split_results = my_files[i].split('.')
        file_name = '.'.join([split_results[0] + '_copy', split_results[1]])
        # 保存文件
        with open(FILE_OUT_PATH + file_name, 'wb') as f:
            f.write(img_data)