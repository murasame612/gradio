import json
import os
from model import get_all_file_paths

def save_in_user(user:str):
    os.makedirs(f"user/{user}/history/",exist_ok=True)
    history_path = f"user/{user}/history/his.json"
    json_list  = get_all_file_paths(f"user/{user}/latest/json")
    e_sum = len(json_list)
    correct_sum = 0
    for j_path in json_list:
        with open(j_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data["correct"]:
            correct_sum += 1

    if not os.path.exists(history_path):
        with open(history_path, 'w',encoding='utf-8') as f:
            json.dump({"total":e_sum,"correct":correct_sum},f,indent=4)
    else:
        with open(history_path, 'r', encoding='utf-8') as f:
            his = json.load(f)
        his["total"] += e_sum
        his["correct"] += correct_sum
        with open(history_path, 'w',encoding='utf-8') as f:
            json.dump(his,f,indent=4)

def gen_ala_html(user:str):
    with open(f"user/{user}/history/his.json", 'r', encoding='utf-8') as f:
        his = json.load(f)
    acc = his["correct"]/his["total"]*100
    html_content = f"""
        <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>正确率进度条</title>
        <style>
            .progress-container {{
        width: 100%; /* 容器宽度 */
                background-color: #e0e0e0; /* 容器背景色 */
                border-radius: 10px; /* 圆角 */
                height: 30px; /* 进度条高度 */
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 阴影 */
            }}
            
            .progress-bar {{
        height: 100%; /* 进度条填满容器 */
                width: 0; /* 初始宽度 */
                border-radius: 10px; /* 圆角 */
                text-align: center; /* 文字居中 */
                line-height: 30px; /* 文字垂直居中 */
                color: white; /* 文字颜色 */
                font-weight: bold; /* 字体加粗 */
                transition: width 0.3s ease; /* 动画过渡 */
            }}
            
            .progress-bar.red {{
        background-color: red; /* 低于 60% 时的颜色 */
            }}
            
            .progress-bar.yellow {{
        background-color: yellow; /* 80% 以下时的颜色 */
                color: black; /* 黄色时文字颜色改为黑色 */
            }}
            
            .progress-bar.green {{
        background-color: green; /* 高于 80% 时的颜色 */
            }}
        </style>
    </head>
    <body>
        <h3>正确率进度条</h3>
        <div class="progress-container">
            <div class="progress-bar" id="progress-bar">0%</div>
        </div>
    
        <script>
            // 设置正确率
            var accuracy = f{acc}; // 你可以修改此值（例如 59, 80, 90 等）
            
            var progressBar = document.getElementById('progress-bar');
            progressBar.style.width = accuracy + '%'; // 设置进度条宽度
            progressBar.innerHTML = accuracy + '%'; // 显示正确率
    
            // 根据正确率设置颜色
            if (accuracy < 60) {{
        progressBar.classList.add('red');
        }} else if (accuracy < 80) {{
        progressBar.classList.add('yellow');
        }} else {{
        progressBar.classList.add('green');
        }}
        </script>
    </body>
    </html>

    """
    return html_content
