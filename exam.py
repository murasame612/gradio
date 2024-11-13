from ultralytics import YOLO
from PIL import Image

# 加载 YOLO 模型
model = YOLO("C:/Users/chenj/Documents/GitHub/ultralytics/runs/obb/train8/weights/best.pt")

def detect(image):
    if image is None:
        return None
    # 进行检测
    results = model(image)
    # 获取检测结果并转换为 PIL 图像
    result_image = results[0].plot()  # 使用 plot() 方法获取带有检测结果的图像
    return Image.fromarray(result_image)
