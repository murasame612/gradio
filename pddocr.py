import json

import cv2
from paddlex import create_model
import os

from model import get_all_file_paths
import re
from model import clear_folder


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


def ocr_and_save(user: str, img_path: str):
    """
    进行OCR识别并保存结果和图片到指定用户的latest文件夹

    @param user: str, 用户名
    @param img_path: str, 图片路径
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
        index, _ = os.path.splitext(img_name)
        res.save_to_img(os.path.join(save_path, "image", f"{index}.png"))
        res.save_to_json(os.path.join(save_path, "json", f"{index}.json"))


def process_wrong_image(user: str):
    """
    对用户的图片进行OCR识别，并保存结果
    @param user: str, 用户名
    """
    # 获取用户最新的图片
    json_path = os.path.join("./user", user, "latest", "json")
    json_list = get_all_file_paths(json_path)

    for j in json_list:
        json_file_path = j

        # 打开文件并读取JSON内容
        with open(json_file_path, 'r', encoding='GBK') as f:
            data = json.load(f)
        text = data["rec_text"]
        equality = convert_wrong_char(text)
        data["equality"] = "".join(equality)
        is_correct = equality_correct(equality)[0]
        res = equality_correct(equality)[1]
        if is_correct == "True":
            data["correct"] = True
        else:
            data["correct"] = False

        data["result"] = res
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)

        if data["rec_score"] < 0.7:
            os.remove(json_file_path)
            img_path = json_file_path.replace(".json", ".png")
            img_path_1 = img_path.replace("json", "image")
            os.remove(img_path_1)


def convert_wrong_char(equality: str) -> list:
    #替换规则
    parts = re.split(r'([÷+\-x×X=])', equality)
    #数字序列
    num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    #替换表
    trans_table = str.maketrans({
        "/": "1",
        "b": "6",
        "(": "1",
        ")": "7",
        "s": "5",
        "S": "5",
        "%": "4",
        "}": "1",
        "{": "1",
        "[": "1",
        "]": "1",
        "a": "0",
        "π": "=",
        "c": "5",
        "C": "5",
        " ": "",
        ":": ".",
        "D": "0",
        "O": "0",
        "o": "0",
        't': "4",
    })
    equality_list = [part.strip() for part in parts if part.strip()]
    for i, num in enumerate(equality_list):
        num = num.translate(trans_table)
        #如果是数字，清理可能会出现前置或后置非数字字符
        if i in [0, 2, 4]:
            if num[0] not in num_list:
                num = num[1:]
            if num[-1] not in num_list:
                num = num[:-1]
        equality_list[i] = num
    return equality_list


def equality_correct(equal_list: list):
    print("is_correct?: ", equal_list)
    try:
        a, opr, b, _, res = equal_list
        a, b, res = eval(a), eval(b), eval(res)
    except SyntaxError:
        print("符号错误于：", equal_list)
        return "False","识别错误"
    except ValueError:
        print("数值错误于：", equal_list)
        return "False","识别错误"
    except NameError:
        print("名称错误于：", equal_list)
        return "False","识别错误"

    output = "False"
    sppose = 0
    theresold = 0.001  #容许的误差
    if opr == '+':
        sppose = a + b
        if abs(a + b - res) <= theresold:
            print(abs(a + b - sppose))
            output = "True"
    elif opr == '-':
        sppose = a - b
        if abs(a - b - res) <= theresold:
            print(abs(a - b - res))
            output = "True"
    elif opr in ['x', "X", "×"]:
        sppose = a * b
        if abs(a * b - res) <= theresold:
            print(abs(a * b - res))
            output = "True"
    elif opr == '÷':
        sppose = a / b
        if abs(a / b - res) <= theresold:
            print(abs(a / b - sppose))
            output = "True"

    return output, sppose

