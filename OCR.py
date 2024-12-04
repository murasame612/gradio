import os
import pytesseract
import cv2

custom_oem_psm_config = r' --oem 1 --psm 4 -l num'  # 修改为你自定义模型所在目录

def preprocess_image(img_path):
    # 读取图像
    ima = cv2.imread(img_path)
    denoised_img = cv2.medianBlur(ima, 1)
    # 转为灰度图
    gray_img = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2GRAY)
    # 调整大小（根据需求，可以修改宽高）
    binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 5)
    resized_img = cv2.resize(binary_img, (300, 60))
    return resized_img

def ocr(img_path):
    # 图像预处理
    image = preprocess_image(img_path)
    # 使用自定义模型进行文字识别
    recognized_text = pytesseract.image_to_string(image, config=custom_oem_psm_config)
    return recognized_text

import easyocr

def ocr_with_easyocr(img_path):
    # 创建 EasyOCR 阅读器实例
    reader = easyocr.Reader(['en'])  # 这里指定语言为英语，如果需要其他语言，可以添加对应的语言代码，如 ['ch_sim']（简体中文）
    img = preprocess_image(img_path)
    # 使用 easyocr 进行文字识别
    result = reader.readtext(img)

    # 解析识别结果
    recognized_text = ""
    for (bbox, text, prob) in result:
        recognized_text += f"Detected text: {text} (Confidence: {prob*100:.2f}%)\n"

    return recognized_text


class equality:
    def __init__(self,img,text,user):
        self.img = img
        self.text = text
        self.user = user
        self.folder_path = os.path.join("user",self.user,"image")

    def __len__(self):
        count = 0
        for filename in os.listdir(self.folder_path):
            if filename.startswith("equality") and filename.endswith(('.png', '.jpg', '.jpeg')):
                count += 1
        return count

    def html(self):
        return f"<src= https://172.0.0.1/image/{self.user}/image>"



from PIL import Image

def modify_and_save_multitiff(input_tiff_path, output_tiff_path,new_dpi=(300, 300)):
    """
    修改多页 TIFF 文件，并保存为新的多页 TIFF 文件，同时修改每页的 DPI。

    参数：
    - input_tiff_path: 输入的多页 TIFF 文件路径
    - output_tiff_path: 输出的修改后多页 TIFF 文件路径
    - modify_function: 一个接受单页图像并返回修改后的图像的函数
    - new_dpi: 新的 DPI 值，默认 (300, 300)

    返回：
    - None
    """

    # 打开输入的多页 TIFF 文件
    with Image.open(input_tiff_path) as img:
        # 获取 TIFF 文件的页数
        num_pages = img.n_frames

        # 创建一个列表，用于存储修改后的每一页图像
        modified_images = []

        # 循环遍历每一页
        for page in range(num_pages):
            img.seek(page)  # 跳转到当前页面
            modified_image = img.copy()  # 复制当前页图像

            # 使用传入的修改函数修改当前图像

            # 修改图像的 DPI
            modified_image.info['dpi'] = new_dpi

            # 将修改后的图像添加到列表中
            modified_images.append(modified_image)

        # 保存修改后的图像为多页 TIFF 文件
        modified_images[0].save(output_tiff_path, save_all=True, append_images=modified_images[1:], resolution=new_dpi[0], compression='tiff_deflate')

    print(f"修改后的多页 TIFF 文件已保存为: {output_tiff_path}")


# 使用示例：


if __name__ == "__main__":
    # print(list(ocr("train_ocr/image/equality3.png")))
    print(ocr_with_easyocr("train_ocr/image/equality16.png"))
    # input_path = 'train_ocr/processed_image/num.tif'
    # output_path = 'train_ocr/processed_image/dpi.tif'
    # 设置新的 DPI 为 300x300
    # modify_and_save_multitiff(input_path, output_path, new_dpi=(300, 300))


