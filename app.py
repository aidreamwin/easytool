import gradio as gr
import numpy as np
from image.gaussian_compare import image_process

class Args():
    def __inint__(self):
        self.input = None
        self.radius = 5

def gaussianBlur(input_img, radius):
    args = Args()
    args.input = input_img
    args.radius = radius
    print(input_img)
    dst_file = image_process.process(args)
    return dst_file, dst_file

image_input = gr.Image(label="Image", type="filepath")
number_input = gr.Slider(label="Input Number", minimum=0, maximum=50, value=5, step=1)
output_image = gr.Image(label="Output Image", type="filepath")
output_file = gr.File(label="Download Image")

demo = gr.Interface(gaussianBlur, inputs=[image_input, number_input], outputs=[output_image, output_file], allow_flagging="never")
demo.launch(server_name="0.0.0.0", server_port=28999)