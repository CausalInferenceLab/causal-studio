import os
from IPython.display import Image, display

path_image = '/Users/jiwoo/3_스터디/가짜연구소 12기/Causal Studio/3_code/image'

def show_image(filename, path=path_image):
    full_path = os.path.join(path_image, filename)
    display(Image(filename=full_path))