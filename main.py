import gradio as gr
import os
from getSum import gen_ala_html
import getSum
import processImage
import threading
from model import delete_his_json

# 初始化状态字典，包含默认值
initDic = {"登录" :0,"user":""}
state = gr.State(initDic)



def save_user(User: str):
    """
    处理用户登录和注册。

    参数:
        User (str): 用户提供的用户名。

    返回:
        list: 一组 Gradio 更新对象，用于根据登录/注册状态更新 UI。
        outputs=[user_output,user,user_button,exist_button,deny_button]
    """
    if User == "" or len(User) >= 10:
        return [f"{User} 用户名不合法",gr.update(visible=True),gr.update(visible=True),gr.update(visible=False),
                gr.update(visible=False),gr.update(value=state.value["user"])]

    if state.value["登录"]==0:
        if os.path.exists(f"User/{User}"):
            if os.path.isdir(f"User/{User}"):
                state.value["user"] = User
                return [f"{User}已登录",gr.update(visible=False),gr.update(visible=False),gr.update(visible=True),
                        gr.update(visible=False),gr.update(value=state.value["user"])]

        else:
            state.value["登录"] =1
            return [f"{User} 用户不存在,是否要注册？",gr.update(visible=False),gr.update(value="注册"),gr.update(visible=False),
                    gr.update(visible=True),gr.update(value=state.value["user"])]
    else:
        os.makedirs(f"user/{User}")
        state.value["user"] = User
        state.value["登录"] =0
        return [f"{User} 已经注册并登录",gr.update(visible=False),gr.update(visible=False),gr.update(visible=True),
                gr.update(visible=False),gr.update(value=state.value["user"])]


def exist():
    """
    处理用户登出。

    返回:
        list: 一组 Gradio 更新对象，用于根据登出状态更新 UI。
    """
    state.value["user"]="public"
    return [gr.update(visible=True),#user_b：登录按钮可见
            gr.update(visible=True),#user：登录输入框可见
            gr.update(visible=False),#exist_b：登出按钮不可见
            gr.update(value="已退出登录"),#日志输出框：更新为“登出”
            gr.update(value=state.value["user"])]


def denied():
    """
    处理注册取消。

    返回:
        list: 一组 Gradio 更新对象，用于根据注册取消状态更新 UI。
    """
    state.value["登录"] =0
    state.value["user"] = "public"
    return [gr.update(value="登录"),gr.update(visible=False),gr.update(value="注册已取消"),gr.update(visible=True),gr.update(value=state.value["user"])]
    #注册（user_button）还原为登录，deny_button隐藏,日记提示取消，输入框再现

with gr.Blocks(title="自动批改",theme="soft",css="style.css") as demo:
    hidden_user = gr.Textbox("public",visible=False,interactive=False)
    with gr.Row(elem_classes="custom-row"):
    # gr.Markdown("## 欢迎使用自动批改系统")
        with gr.Column():
            gr.HTML("<h1 class='blue-text simple-blue-text'>欢迎使用自动批改系统</h1>")
            gr.HTML("<h1 class='arc-blue-text'>请上传和拍摄图片来得到分析报告。如果要在系统得到保存，请先输入你的用户名。</h1>")
        with gr.Column():
            user = gr.Textbox(value="用户名")
            user_output = gr.Textbox(label="日记",interactive=False)
            user_button = gr.Button("登录",visible=True,elem_classes="gr-button")
            exist_button = gr.Button("退出登录",visible=False,elem_classes="red-button")
            deny_button = gr.Button("取消",visible=False,elem_classes="red-button")

    # 定义按钮点击动作
    user_button.click(fn=save_user, inputs=user, outputs=[user_output, user, user_button, exist_button, deny_button,hidden_user])
    exist_button.click(fn=exist,outputs=[user_button,user,exist_button,user_output,hidden_user])
    deny_button.click(fn=denied,outputs=[user_button,deny_button,user_output,user,hidden_user])


    with gr.Tab(label = "拍照上传"):
        with gr.Row(elem_classes="custom-row"):
            with gr.Column(scale=1):
                gr.HTML("<h1 class='arc-blue-text'>请在右边上传图像</h1>"
                        "<br>会在下方产生此次上传的识别结果<br>"
                        "你可以给排除错误的识别<br><br>")
                submit_button = gr.Button("上传图片",elem_classes="blue-button")
            
            inputIma=gr.Image(scale=2,height=300)
            result = gr.Image(interactive=False,scale=2,height=300)
        #处理图片并保存图片到User/用户名/image
        his_button = gr.Button(value = "已经检查批改内容")
        html_output = gr.HTML()
        submit_button.click(fn= processImage.detect,inputs=[inputIma,hidden_user],outputs=[result,html_output],)
        his_button.click(fn=getSum.save_in_user,inputs=hidden_user)
    #存放历史照片，存储路径为User/用户名/image,只有登录后才会出现
    # with gr.Tab(label = "历史记录"):
    #     with gr.Row():
    #         gen_button = gr.Button("生成历史记录",elem_classes="blue-button")
    with gr.Tab(label = "分析报告"):
            gen_ala_button = gr.Button(value = "生成分析报告",elem_classes="blue-button")
            delete_his_button = gr.Button(value = "删除历史记录",elem_classes="red-button")
            ala_html_out = gr.HTML()
            gen_ala_button.click(fn=gen_ala_html,inputs=hidden_user,outputs=ala_html_out)
            delete_his_button.click(fn=delete_his_json,inputs=hidden_user,outputs=ala_html_out)


def gradio_main():
    demo.launch(debug=True,share=True)

from static_photo import flask_main

if __name__ == "__main__":
    gr_thread = threading.Thread(target=gradio_main)
    flask_thread = threading.Thread(target=flask_main)
    gr_thread.start()
    flask_thread.start()
    flask_thread.join()
    gr_thread.join()