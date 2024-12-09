import json
import os
from model import get_all_file_paths

def save_in_user(user:str):
    os.makedirs(f"user/{user}/history/",exist_ok=True)
    history_path = f"user/{user}/history/his.json"
    json_list  = get_all_file_paths(f"user/{user}/latest/json")
    e_sum = len(json_list)
    correct_sum = 0
    mul_sum = 0
    div_sum =0
    add_sum = 0
    minus_sum = 0
    mul_correct_sum = 0
    div_correct_sum = 0
    add_correct_sum = 0
    minus_correct_sum = 0
    #一次性统计latest目录下的json文件
    #-------------------------------------------------
    #统计四则运算正确数和总数，还有总共正确数
    for j_path in json_list:
        with open(j_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data["equality_operator"] == "mul":
            mul_sum += 1
            if data["correct"]:
                mul_correct_sum += 1
                correct_sum += 1
        elif data["equality_operator"] == "div":
            div_sum += 1
            if data["correct"]:
                div_correct_sum += 1
                correct_sum += 1
        elif data["equality_operator"] == "add":
            add_sum += 1
            if data["correct"]:
                add_correct_sum += 1
                correct_sum += 1
        elif data["equality_operator"] == "minus":
            minus_sum += 1
            if data["correct"]:
                minus_correct_sum += 1
                correct_sum += 1
    #-------------------------------------------

    if not os.path.exists(history_path):
        with open(history_path, 'w',encoding='utf-8') as f:
            json.dump({"total":e_sum,"correct":correct_sum,
                       "div_sum":div_sum,"add_sum":add_sum,"mul_sum":mul_sum,"minus_sum":minus_sum,
                       "div_correct_sum":div_correct_sum,"add_correct_sum":add_correct_sum,
                       "mul_correct_sum":mul_correct_sum,"minus_correct_sum":minus_correct_sum},f,indent=4)
    else:
        with open(history_path, 'r', encoding='utf-8') as f:
            his = json.load(f)
        his["total"] += e_sum
        his["correct"] += correct_sum
        his["div_sum"] += div_sum
        his["add_sum"] += add_sum
        his["mul_sum"] += mul_sum
        his["minus_sum"] += minus_sum
        his["div_correct_sum"] += div_correct_sum
        his["add_correct_sum"] += add_correct_sum
        his["mul_correct_sum"] += mul_correct_sum
        his["minus_correct_sum"] += minus_correct_sum
        with open(history_path, 'w',encoding='utf-8') as f:
            json.dump(his,f,indent=4)

def gen_ala_html(user: str):
    import json

    # 读取 JSON 文件
    if os.path.exists(f"user/{user}/history/his.json"):
        with open(f"user/{user}/history/his.json", 'r', encoding='utf-8') as f:
            his = json.load(f)
    else:
        return "<p>你还没有提交记录</p>"
    # 计算正确率
    acc = his["correct"] / his["total"]
    if his["add_sum"] == 0:
        add_acc = "无数据"
    else:
        add_acc = his["add_correct_sum"] / his["add_sum"]
        add_acc//=0.01
    if his ["div_sum"] == 0:
        div_acc = "无数据"
    else:
        div_acc = his["div_correct_sum"] / his["div_sum"]
        div_acc//=0.01
    if his["mul_sum"] == 0:
        mul_acc = "无数据"
    else:
        mul_acc = his["mul_correct_sum"] / his["mul_sum"]
        mul_acc//=0.01
    if his["minus_sum"] == 0:
        minus_acc = "无数据"
    else:
        minus_acc = his["minus_correct_sum"] / his["minus_sum"]
        minus_acc//=0.01
    acc //=0.01
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
    
    <p>其中：</p>
    <p>加法正确率为：<strong>{add_acc}%</strong></p>
    <p>减法正确率为：<strong>{minus_acc}%</strong></p>
    <p>乘法正确率为：<strong>{mul_acc}%</strong></p>
    <p>除法正确率为：<strong>{div_acc}%</strong></p>
    
    <p>该结果是根据您的历史数据计算得出的。</p>
</body>
</html>

    """

    return html_content
