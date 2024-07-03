# Easy_SV3D
A Streamlit and slightly modified and enhanced version of Stability AI SV3D

This is a fork from: 

https://github.com/Stability-AI/generative-models

Utilizing the StabilityAI SV3D Model:

https://huggingface.co/stabilityai/sv3d

With slight modifications to the simple_video_sample.py file to use FFMPEG 

## Setup virtual enviroment
``` console
$ 
$ python3 -m venv VIRUTALVENV
$ source VIRTUALENV/bin/activate
(VIRTUALENV) $ pip install pt2.txt
(VIRTUALENV) $ git clone https://github.com/automateyournetwork/Easy_SV3D.git
(VIRTUALENV) $ cd Easy_SV3D
(VIRTUALENV) ~/Easy_SV3D$ streamlit run easy_sv3d.py
```

### Visit localhost:8501

Type in a prompt for your image 

Select from dropdown menus 

Upload an image

### Best Results
Images with a solid white background perform the best. This code adds to your prompt (user manually typed or drop down selections) to try and force the image generation to make an image with a solid white background. 

### Samples
Some wonderful samples can be downloaded from 

https://sv3d.github.io/index.html?page=0#gallery-3d

