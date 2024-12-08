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

def gen_ala_html(user: str):
    import json

    # 读取 JSON 文件
    with open(f"user/{user}/history/his.json", 'r', encoding='utf-8') as f:
        his = json.load(f)

    # 计算正确率
    acc = his["correct"] / his["total"] * 100
    acc //=0.01
    acc/=100
    print("acc:-------------------------->", acc)

    # 创建 HTML 内容
    html_content = f"""
        <!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>正确率展示</title>
</head>
<body>
    <h3>正确率展示</h3>
    
    <p>您的当前正确率为：</p>
    
    <p><strong>{acc}%</strong></p>
    
    <p>该结果是根据您的历史数据计算得出的。</p>
</body>
</html>

    """

    return html_content
