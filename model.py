import gradio as gr

def initialize_state():
    return {'counter1': 0, 'counter2': 0}

def increment_counters(state, increment1, increment2):
    state['counter1'] += increment1
    state['counter2'] += increment2
    return state['counter1'], state['counter2']

def reset_counters(state):
    state.value['counter1'] = 0
    state.value['counter2'] = 0
    return state['counter1'], state['counter2']

with gr.Blocks() as demo:
    state = gr.State(value=initialize_state())

    with gr.Row():
        increment1 = gr.Number(label="增加计数器1")
        increment2 = gr.Number(label="增加计数器2")
        increment_button = gr.Button("增加")

    with gr.Row():
        counter1_output = gr.Textbox(label="计数器1值")
        counter2_output = gr.Textbox(label="计数器2值")
        reset_button = gr.Button("重置")

    increment_button.click(lambda inc1, inc2: increment_counters(state.value, inc1, inc2),
                           inputs=[increment1, increment2],
                           outputs=[counter1_output, counter2_output])

    reset_button.click(lambda: reset_counters(state.value),
                       inputs=[],
                       outputs=[counter1_output, counter2_output])

demo.launch()
