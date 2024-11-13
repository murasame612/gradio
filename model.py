import gradio as gr

s = gr.State({"s":"a"})
s.value["s"]="b"
print(s.value["s"])