import gradio as gr
import os

import exam

# import exam
initDic = {"登录" :0,"user":None}
state = gr.State(initDic)



def save_user(User: str):
    if User == "" or len(User) >= 10:
        return [f"{User} 用户名不合法",gr.update(visible=True),gr.update(visible=True),gr.update(visible=False),
                gr.update(visible=False)]

    if state.value["登录"]==0:
        if os.path.exists(f"User/{User}"):
            if os.path.isdir(f"User/{User}"):
                state.value["user"] = User
                return [f"{User}已登录",gr.update(visible=False),gr.update(visible=False),gr.update(visible=True),
                        gr.update(visible=False)]
                #outputs=[user_output,user,user_button,exist_button,deny_button]
        else:
            state.value["登录"] =1
            return [f"{User} 用户不存在,是否要注册？",gr.update(visible=False),gr.update(value="注册"),gr.update(visible=False),
                    gr.update(visible=True)]
    else:
        os.makedirs(f"user/{User}")
        cur_user = User
        state.value["登录"] =0
        return [f"{cur_user} 已经注册并登录",gr.update(visible=False),gr.update(visible=False),gr.update(visible=True),
                gr.update(visible=False)]


def exist():
    return [gr.update(visible=True),gr.update(visible=True),gr.update(visible=False),gr.update(value="已退出登录")]
    #user_b：登录按钮可见，user：登录输入框可见，exist_b：登出按钮不可见，日志输出框：更新为“登出”

def denied():
    state.value["登录"] =0
    return [gr.update(value="登录"),gr.update(visible=False),gr.update(value="注册已取消"),gr.update(visible=True)]
    #注册（user_button）还原为登录，deny_button隐藏,日记提示取消，输入框再现

with gr.Blocks(title="自动批改",theme="soft",css_paths="style.css") as demo:
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

    user_button.click(fn=save_user, inputs=user, outputs=[user_output, user, user_button, exist_button, deny_button])
    exist_button.click(fn=exist,outputs=[user_button,user,exist_button,user_output])
    deny_button.click(fn=denied,outputs=[user_button,deny_button,user_output,user])


    with gr.Tab(label = "拍照上传"):
        with gr.Row(elem_classes="custom-row"):
            with gr.Column(scale=1):
                gr.HTML("<h1 class='arc-blue-text'>请在右边上传图像</h1>"
                        "<br>会在下方产生此次上传的识别结果<br>"
                        "你可以给每个识别结果进行排除错误的<br><br>")
                submit_button = gr.Button("上传图片",elem_classes="blue-button")
            inputIma=gr.Image(scale=3,height=300)
            result = gr.Image(interactive=False,scale=3,height=300)
        submit_button.click(fn= exam.detect,inputs=inputIma,outputs=result)


    with gr.Tab(label = "历史记录"):
        with gr.Row():
            gr.Image()
    with gr.Tab(label = "分析报告"):
        with gr.Row():
            gr.Image()

demo.launch(debug=True)
