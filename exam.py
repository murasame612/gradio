from ultralytics import YOLO
from PIL import Image
import os

# 加载 YOLO 模型
model = YOLO("C:/Users/chenj/Documents/GitHub/ultralytics/runs/obb/train8/weights/best.pt")

#保存图片
def detect(image,user):
    if image is None:
        return None
    save_path =os.path.join("./user",user,'image')
    os.makedirs(save_path,exist_ok=True)
    #image是一个ndarray对象，需要转换为PIL对象，并保存
    pil_image = Image.fromarray(image)
    pil_image.save(os.path.join(save_path,"detected_image.png"))

    results = model(image)
    # 获取检测结果并转换为 PIL 图像
    result_image = results[0].plot()  # 使用 plot() 方法获取带有检测结果的图像
    return Image.fromarray(result_image)
