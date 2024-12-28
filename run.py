import os
exec_command = 'pip install setuptools numpy'
    
os.system(exec_command)

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
img = cv2.imread(img_path)
result = ocr.ocr(img)

for line in result:
    line_text = ' '.join([word_info[-1] for word_info in line])
    print(line_text)
    
    #https://paddlepaddle.github.io/PaddleOCR/latest/quick_start.html#1-paddlepaddle
    #https://developer.baidu.com/article/detail.html?id=3314943
