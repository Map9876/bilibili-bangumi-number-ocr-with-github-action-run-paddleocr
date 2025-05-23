import os
import re
import json
import requests
from datetime import datetime
import time
import cv2
from numpy import char
from bs4 import BeautifulSoup
os.system('pip install setuptools numpy==1.26.4 bs4 beautifulsoup4 paddleocr opencv-python')
os.system(' python -m pip install --pre paddlepaddle -i https://www.paddlepaddle.org.cn/packages/nightly/cpu/')   
import paddle

import numpy

import requests
import time
import json
from datetime import datetime
import os
import os

            
exec_command = 'pip install setuptools numpy bs4 beautifulsoup4'

global ok
ok = True
os.system(exec_command)
import bs4
from bs4 import BeautifulSoup
    # 如果库不存在，则执行安装命令 
os.system(exec_command)
exec_command = 'pip uninstall numpy scipy pandas'

exec_command = 'python3 -m pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/'
os.system(exec_command)
exec_command = 'pip install paddleocr'
    
os.system(exec_command)
#exec_command = 'pip install numpy==1.19.3 scipy pandas'
    
#os.system(exec_command)
from paddleocr import PaddleOCR,draw_ocr
import paddle
from paddleocr import PaddleOCR,draw_ocr
c = "curl https://bce.bdstatic.com/p3m/common-service/uploads/wap-article_244e0ff.png -O"   
os.system(c) 
import cv2

ocr = PaddleOCR(lang='ch')
img_path = 'wap-article_244e0ff.png'  # 请替换为你的图片路径

def pip_ocr(img_path, title):
    img = cv2.imread(img_path)
    result = ocr.ocr(img)
    
    with open("README.md", "a")  as f:
        f.write(f"\n\n{title} : \n")
    for i in range(len(result[0])):
    
        print(result[0][i][1][0])
    with open("README.md", "a")  as f:
        f.write(result[0][i][1][0])

        
# 安装所需的库
def install_packages():
    os.system('pip install setuptools bs4 beautifulsoup4 paddleocr')
    os.system('pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/')   

# 下载图片
def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image: {image_url}")

# OCR 识别图片文字
def perform_ocr(img_path):
    #from paddleocr import PaddleOCR, draw_ocrp
    ocr = PaddleOCR(lang='ch')
    img = cv2.imread(img_path)
    result = ocr.ocr(img)
    return result

# 查找链接和同层级的其他键值对
def find_links_and_siblings(data):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                results.extend(find_links_and_siblings(value))
            elif isinstance(value, str):
                if re.match(r'https://activity.hdslb.com/.*\.(zip|rar)', value):
                    parent = data
                    siblings = {k: v for k, v in parent.items() if k != key}
                    results.append((value, siblings))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_links_and_siblings(item))
    return results

# 处理每个链接和图片，执行 OCR 并存储数据
def process_links_and_images(links_and_siblings):
    data_list = []
    for link, siblings in links_and_siblings:
        image_url = siblings.get('image')
        if image_url:
            image_url = image_url.lstrip('//')
            image_path = f"images/{os.path.basename(image_url)}"
            os.mkdir("./images")
            download_image(f"https://{image_url}", image_path)
            ocr_result = perform_ocr(image_path)

            text_result = "\n".join([res[1][0] for res in ocr_result[0]])
            data_list.append({
                "original_link": link,
                "image_link": image_url,
                "text": text_result
            })

            with open("README.md", "a") as f:
                f.write(f"\n\n{siblings.get('title', 'No Title')} : \n{text_result}")

    return data_list

# 主函数，解析 HTML 并提取数据
def main():
    #install_packages()

    headers = {
    'authority': 'data.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/blackboard/newplayer.html?aid=113860405104772&autoplay=0&crossDomain=1&as_wide=1&poster=0',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    # 给定的URL
    url = "https://www.bilibili.com/blackboard/era/lzdxvghInSo4oYjm.html?i_transfer_match=db4c84ad-1367-4f82-a06c-31d8cbc15d29&native.theme=1&share_source=copy&share_medium=android&bbid=4C7C116F-8EEA-F382-688C-E66CD58CE4A509839infoc&ts=1737666592222"

    # 发送请求获取HTML内容
    response = requests.get(url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', string=re.compile(r'window.__BILIACT_EVAPAGEDATA__\s*=\s*'))

    if script_tag:
        lines = str(script_tag).split('\n')
        for line in lines:
            if 'window.__BILIACT_EVAPAGEDATA__' in line:
                json_text = line.split('window.__BILIACT_EVAPAGEDATA__ = ')[1].strip().rstrip(';')
                break

        data = json.loads(json_text)
        links_and_siblings = find_links_and_siblings(data)
        data_list = process_links_and_images(links_and_siblings)
        print("处理完成的数据:", data_list)
    else:
        print("未找到 window.__BILIACT_EVAPAGEDATA__ 变量")

if __name__ == "__main__":
    main()
