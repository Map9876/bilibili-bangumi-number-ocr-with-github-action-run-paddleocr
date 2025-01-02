import requests
import time
import json
from datetime import datetime
import os
import os

            
exec_command = 'pip install setuptools numpy bs4 beautifulsoup4'
ok = True
global ok
ok = "随便"
os.system(exec_command)
import bs4
from bs4 import BeautifulSoup
    # 如果库不存在，则执行安装命令 
exec_command = 'python3 -m pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/'
os.system(exec_command)
exec_command = 'pip install paddleocr'
    
os.system(exec_command)
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
        

#https://paddlepaddle.github.io/PaddleOCR/latest/quick_start.html#1-paddlepaddle
    #https://developer.baidu.com/article/detail.html?id=3314943





# Headers for requests
import requests
import time
import json
from datetime import datetime
import os
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

# Function to get video list
def get_video_list(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch video list: {response.status_code}")

# Function to get permanent link
def get_permanent_link(url):
    response = requests.get(url, headers=headers, allow_redirects=True)
    if 'location' in response.headers:
        print(response.url)
        return get_permanent_link(response.headers['location'])
    else:
        print(response.url)
        return response.url

# Function to get video download url using ep_id
def get_video_download_link(ep_id):
    headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    params = {
    'ep_id': ep_id,
    'bsource': '',
    }

    api_url = f"https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id={ep_id}&bsource="
    response = requests.get('https://api.bilibili.com/pgc/player/web/playurl/html5', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0 and 'result' in data:
            return data['result']['durl'][0]['url']
        else:
            print(f"Failed to fetch video download link: {data['message']}, {api_url}, {response.text}")
            return None
    else:
        print(f"Failed to fetch video download link: {response.status_code}")
        return None

# Function to download video
def download_video(url, filename):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        raise Exception(f"Failed to download video: {response.status_code}")

# Function to capture screenshot
def capture_screenshot(video_path, time_point, output_path):
    os.system(f"yes | ffmpeg -ss {time_point} -i {video_path} -vf 'crop=iw/4:ih/6:iw*3/4:ih*5/6' -frames:v 1 {output_path} -loglevel quiet 1 ")
def get_ep_id_from_page(url, headers):
    final_url = get_permanent_link(url)
    response = requests.get(final_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    if ok is True:
        print(response.text)
        ok = False
    # Find the script tag with id __NEXT_DATA__
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    
    if script_tag:
        # Load the JSON content from the script tag
        import json
        json_content = json.loads(script_tag.string)
        
        # Navigate to the desired part of the JSON structure
        try:
            ep_info = json_content['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['result']['play_view_business_info']['episode_info']
            ep_id = ep_info['ep_id']
            return ep_id
        except:
            return None
def main():
    global ok
    ok = True
    video_list_url = "https://app.bilibili.com/x/v2/space/archive/cursor?vmid=928123"
    video_data = get_video_list(video_list_url)
    items = video_data['data']['item']

    for item in items:
        print()
        print()
        bvid = item['bvid']
        title = item['title']
        title = title.replace("/", "")
        
        temporary_link = f"https://m.bilibili.com/video/{bvid}"
        print(title)
        # Get permanent link
        """
        permanent_link = get_permanent_link(temporary_link)
        print(permanent_link)这里得到ep链接
        
        # Extract ep_id from permanent link
        ep_id = permanent_link.split('ep')[-1]
     #   ep_id变成了https://m.bilibili.com/video/BV1NTkXYMEjA
        # Get video download link
        """
        
        ep_id = get_ep_id_from_page(temporary_link, headers)
        print("检查ep_id点",ep_id)
        video_download_url = get_video_download_link(ep_id)
        
        if video_download_url:
            # Download video
            filename = f"{title}.mp4"
            download_video(video_download_url, filename)
            
            # Capture screenshots
            screenshot1 = f"{title}_screenshot_4s.png"
            screenshot2 = f"{title}_screenshot_8s.png"
            capture_screenshot(filename, "00:00:04", screenshot1)
           # pip_
            capture_screenshot(filename, "00:00:08", screenshot2)
        else:
            print(f"Skipping video {title} due to download link fetch failure")
main()
