import json

from flask import Flask, send_from_directory, send_file, request, jsonify
import os

"""
使用flask解决gradio无法实现的功能
"""
app = Flask(__name__)

@app.route('/<path:user>/image/<path:filename>')
def serve_image(user,filename):
    """
    静态托管图片
    :param user:
    :param filename:
    :return:
    """
    absolute_path = os.path.join(f'D:\pythonproject\gradio\\user\\{user}\\latest\\image', filename)
    return send_file(absolute_path)

@app.route('/<path:user>/json/<path:filename>')
def serve_json(user,filename):
    """
    静态托管json文件
    :param user:
    :param filename:
    :return:
    """
    absolute_path = os.path.join(f'D:\pythonproject\gradio\\user\\{user}\\latest\\json', filename)
    return send_file(absolute_path)

@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    """
    点击按钮后的处理函数,按钮功能是将记录改成正确的,即将json文件中的correct字段改为True
    :return:
    """
    #按钮返回的json数据
    data = request.get_json()
    #获得图片名
    image_name = data.get('image_name')
    #获得用户名
    user = data.get("user")
    #获得图片的json文件名
    j_name = image_name.replace(".png", ".json")
    #根据user图片的json文件路径
    json_file_path = os.path.join("./user", user, "latest", "json",j_name)
    #打开json文件
    with open(json_file_path, 'r', encoding='GBK') as f:
        data = json.load(f)
    #将json文件中的correct字段改为True
    data["correct"] = True
    #写回json
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"{image_name} correct")
    # 可以返回一个响应
    return jsonify({"status": "success", "image_name": image_name,"user":user})

@app.route('/<user>')
def show_images(user):
    """
    生成用户的HTML页面
    :param user:
    :return:
    """
    html_path = os.path.join("./user",user,"images_gallery.html")
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

if __name__ == '__main__':
    app.run(debug=True)

def flask_main():
    """
    启动flask函数，方便使用线程
    :return:
    """
    app.run(port=5000)
