from copyreg import remove_extension

import cv2
from paddlex import create_model
import os


def preprocess_image(img_path):
    # 读取图像
    ima = cv2.imread(img_path)
    denoised_img = cv2.medianBlur(ima, 3)
    # 转为灰度图
    gray_img = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2GRAY)
    # 调整大小（根据需求，可以修改宽高）
    binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 5)
    resized_img_rgb = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2RGB)
    return resized_img_rgb

model = create_model("PP-OCRv4_mobile_rec")

def ocr_and_save(user:str, img_path:str):
    """
    进行OCR识别并保存结果和图片到指定用户的latest文件夹

    @param user: str, 用户名
    @param img_path: str, 图片路径
    @param index: 编号
    """
    # 创建保存路径
    save_path = os.path.join("./user", user, "latest")
    os.makedirs(save_path, exist_ok=True)

    # 进行OCR识别
    result_img = preprocess_image(img_path)
    outputs = model.predict(result_img, batch_size=1)

    # 保存OCR识别结果
    for res in outputs:
        img_name = os.path.basename(img_path)
        index,_ = os.path.splitext(img_name)
        res.save_to_img(os.path.join(save_path, "image", f"{index}.png"))
        res.save_to_json(os.path.join(save_path, "json", f"{index}.json"))



