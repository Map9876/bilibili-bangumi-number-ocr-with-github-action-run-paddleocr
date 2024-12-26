try: 
    import paddlepaddle
    from paddleocr import PaddleOCR,draw_ocr 
    print("paddlepaddle - gpu库已经存在，不需要安装。") 
except ModuleNotFoundError: 
    # 如果库不存在，则执行安装命令 
    exec_command = 'python -m pip install paddlepaddle-gpu==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/'  
    exec(exec_command)
    exec_command = 'pip install paddleocr'
    
    exec(exec_command)

c = "curl https://bce.bdstatic.com/p3m/common-service/uploads/wap-article_244e0ff.png -O"   
 
import cv2

ocr = PaddleOCR(use_gpu=False, lang='en')
img_path = 'wap-article_244e0ff.png'  # 请替换为你的图片路径
img = cv2.imread(img_path)
result = ocr.ocr(img, use_gpu=False)

for line in result:
    line_text = ' '.join([word_info[-1] for word_info in line])
    print(line_text)
    
    #https://paddlepaddle.github.io/PaddleOCR/latest/quick_start.html#1-paddlepaddle
    #https://developer.baidu.com/article/detail.html?id=3314943
