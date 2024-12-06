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
    # ���ݴ��ݵ�ͼƬ����ִ����Ӧ�� Python ����
    print(f"Python function called for {image_name}")
    # ���Է���һ����Ӧ
    return jsonify({"status": "success", "image_name": image_name})

if __name__ == '__main__':
    app.run(debug=True)

def flask_main():
    app.run(port=5000)
