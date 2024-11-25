import gradio as gr


state = gr.State("0")

def test(tst:str,state):
    return state.value["test"]
    

with gr.Blocks() as b:
    but = gr.Button("登录")
    out = gr.Textbox("test")
    but.click(fn=test, inputs=[out,state], outputs=[out])
    
b.launch()