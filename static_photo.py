import json

from flask import Flask, send_from_directory, send_file, request, jsonify
import os

app = Flask(__name__)

@app.route('/<path:user>/image/<path:filename>')
def serve_image(user,filename):
    absolute_path = os.path.join(f'D:\pythonproject\gradio\\user\\{user}\\latest\\image', filename)
    return send_file(absolute_path)

@app.route('/<path:user>/json/<path:filename>')
def serve_json(user,filename):
    absolute_path = os.path.join(f'D:\pythonproject\gradio\\user\\{user}\\latest\\json', filename)
    return send_file(absolute_path)

@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    data = request.get_json()
    image_name = data.get('image_name')
    user = data.get("user")
    # 根据传递的图片名称执行相应的 Python 函数
    # img_path = os.path.join("./user", user, "latest", "image",image_name)
    # os.remove(img_path)
    j_name = image_name.replace(".png", ".json")
    json_file_path = os.path.join("./user", user, "latest", "json",j_name)
    with open(json_file_path, 'r', encoding='GBK') as f:
        data = json.load(f)
    data["correct"] = True
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"{image_name} correct")
    # 可以返回一个响应
    return jsonify({"status": "success", "image_name": image_name,"user":user})

@app.route('/<user>')
def show_images(user):
    html_path = os.path.join("./user",user,"images_gallery.html")
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

@app.route('/call_bottom_function', methods=['POST'])
def call_bottom_function():
    data = request.get_json()
    user = data.get("user")
    print(f"底部按钮被点击，当前用户：{user}")

    # 在这里执行具体的功能
    return jsonify({"status": "success", "user": user})

if __name__ == '__main__':
    app.run(debug=True)

def flask_main():
    app.run(port=5000)
