import os
import random
import streamlit as st
import subprocess
import json
import requests
import yaml
from PIL import Image, ImageOps

# Ensure required keys are initialized
if 'image_prompt' not in st.session_state:
    st.session_state['image_prompt'] = ""
if 'final_video' not in st.session_state:
    st.session_state['final_video'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 1

# Set up the Streamlit app
st.set_page_config(page_title="AI Image and Video Generator", layout="wide")

# Define the function to send requests to the models
def send_request(prompt):
    url = f"http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3",
        "prompt": f"Generate only the prompt with the following details: {prompt}. Do not include anything additional only the prompt.",
        "stream": False,
        "keep_alive": 0
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json().get('response', '')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Load selections from JSON or YAML file
def load_selections(file_path):
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        with open(file_path, 'r') as f:
            selections = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file format. Use JSON or YAML.")
    return selections

# Function to load the next page
def next_page(page_number):
    st.session_state['page'] = page_number
    st.experimental_rerun()

# Page 1: Input image prompt or upload image
def page1():
    st.title("AI Image and Video Generator")
    st.title("Step 1: Enter Image Prompt or Upload Your Image")

    prompt_option = st.radio(
        "Choose how to generate the image prompt:",
        ('Enter manually', 'Use dropdown menus', 'Upload your image')
    )

    selections = load_selections('image_selections.yaml')  # Load from YAML file
    for key in selections:
        selections[key].insert(0, "")
        selections[key].insert(1, "RANDOM")

    uploaded_image = None
    if prompt_option == 'Enter manually':
        image_prompt = st.text_area("Image Prompt", height=200)
        st.session_state['image_prompt'] = image_prompt
    elif prompt_option == 'Upload your image':
        uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        if uploaded_image:
            image = Image.open(uploaded_image)
            image = ImageOps.exif_transpose(image)  # Ensure image is correctly oriented
            image = image.convert("RGB")  # Convert image to RGB format
            image.save("uploaded_image.png")
            st.session_state['image_path'] = "uploaded_image.png"
            st.session_state['image_prompt'] = "User uploaded image"
    else:
        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            setting = st.selectbox("Choose a setting or type your own:", selections['settings'] + ["Other (Type your own)"], key="setting")
            if setting == "RANDOM":
                setting = random.choice(selections['settings'][2:])  # Exclude '' and 'RANDOM' itself
            if setting == "Other (Type your own)":
                setting = st.text_input("Type your own setting:", key="custom_setting")

            character = st.selectbox("Choose a character type or type your own:", selections['characters'] + ["Other (Type your own)"], key="character")
            if character == "RANDOM":
                character = random.choice(selections['characters'][2:])  # Exclude '' and 'RANDOM' itself
            if character == "Other (Type your own)":
                character = st.text_input("Type your own character:", key="custom_character")

            activity = st.selectbox("Choose an activity or type your own:", selections['activities'] + ["Other (Type your own)"], key="activity")
            if activity == "RANDOM":
                activity = random.choice(selections['activities'][2:])  # Exclude '' and 'RANDOM' itself
            if activity == "Other (Type your own)":
                activity = st.text_input("Type your own activity:", key="custom_activity")

            environment = st.selectbox("Choose an environment or type your own:", selections['environments'] + ["Other (Type your own)"], key="environment")
            if environment == "RANDOM":
                environment = random.choice(selections['environments'][2:])  # Exclude '' and 'RANDOM' itself
            if environment == "Other (Type your own)":
                environment = st.text_input("Type your own environment:", key="custom_environment")

            artistic_style = st.selectbox("Choose an artistic style or type your own:", selections['artistic_styles'] + ["Other (Type your own)"], key="artistic_style")
            if artistic_style == "RANDOM":
                artistic_style = random.choice(selections['artistic_styles'][2:])  # Exclude '' and 'RANDOM' itself
            if artistic_style == "Other (Type your own)":
                artistic_style = st.text_input("Type your own artistic style:", key="custom_artistic_style")

        with col2:
            movie = st.selectbox("Choose a movie or type your own:", selections['movies'] + ["Other (Type your own)"], key="movie")
            if movie == "RANDOM":
                movie = random.choice(selections['movies'][2:])  # Exclude '' and 'RANDOM' itself
            if movie == "Other (Type your own)":
                movie = st.text_input("Type your own movie:", key="custom_movie")

            celebrity = st.selectbox("Choose a celebrity or type your own:", selections['celebrities'] + ["Other (Type your own)"], key="celebrity")
            if celebrity == "RANDOM":
                celebrity = random.choice(selections['celebrities'][2:])  # Exclude '' and 'RANDOM' itself
            if celebrity == "Other (Type your own)":
                celebrity = st.text_input("Type your own celebrity:", key="custom_celebrity")

            animal = st.selectbox("Choose an animal or type your own:", selections['animals'] + ["Other (Type your own)"], key="animal")
            if animal == "RANDOM":
                animal = random.choice(selections['animals'][2:])  # Exclude '' and 'RANDOM' itself
            if animal == "Other (Type your own)":
                animal = st.text_input("Type your own animal:", key="custom_animal")

            historic_event = st.selectbox("Choose a historic event or type your own:", selections['historic_events'] + ["Other (Type your own)"], key="historic_event")
            if historic_event == "RANDOM":
                historic_event = random.choice(selections['historic_events'][2:])  # Exclude '' and 'RANDOM' itself
            if historic_event == "Other (Type your own)":
                historic_event = st.text_input("Type your own historic event:", key="custom_historic_event")

            style = st.selectbox("Choose a style or type your own:", selections['styles'] + ["Other (Type your own)"], key="style")
            if style == "RANDOM":
                style = random.choice(selections['styles'][2:])  # Exclude '' and 'RANDOM' itself
            if style == "Other (Type your own)":
                style = st.text_input("Type your own style:", key="custom_style")

        if st.button("Generate Image Prompt", key="generate_prompt"):
            # Combine selected keywords into a simple prompt
            keywords = []
            if character:
                keywords.append(character)
            if activity:
                keywords.append(activity)
            if environment:
                keywords.append(f"in a {environment} setting")
            if setting:
                keywords.append(f"that is {setting}")
            if artistic_style:
                keywords.append(f"in the style of {artistic_style}")
            if movie:
                keywords.append(f"from the movie {movie}")
            if celebrity:
                keywords.append(f"featuring {celebrity}")
            if animal:
                keywords.append(f"with a {animal}")
            if historic_event:
                keywords.append(f"during {historic_event}")
            if style:
                keywords.append(f"with a {style} style")

            keywords_prompt = "using the following keywords can you create a prompt that will generate a single image with a solid white background: " + ", ".join(keywords) if keywords else "a general scene with a solid white background"
            image_prompt = send_request(keywords_prompt)
            st.session_state['generated_image_prompt'] = image_prompt
        else:
            image_prompt = st.session_state.get('generated_image_prompt', '')

        st.text_area("Generated Image Prompt", image_prompt, height=200)
        st.session_state['image_prompt'] = image_prompt

    if st.button("Next", key="next_page1"):
        if st.session_state['image_prompt'] or uploaded_image:
            st.session_state['page'] = 2
            next_page(2)
        else:
            st.error("Please enter a valid image prompt or upload an image.")

# Page 2: Generate and display video
def page2():
    st.title("AI Image and Video Generator")
    st.title("Step 2: Generate and View Video")

    # Keep the elevation constant and only vary azimuth for rotation effect
    constant_elevation = 10.0  # or any suitable constant value
    azimuths_deg = [i * 18.0 for i in range(21)]

    elevations_str = ','.join([str(constant_elevation)] * 21)
    azimuths_str = ','.join(map(str, azimuths_deg))

    if st.button("Generate Video", key="generate_video"):
        input_path = st.session_state.get('image_path', 'uploaded_image.png')
        
        # Call the script
        command = [
            "python", "simple_video_sample.py",
            "--input_path", input_path,
            "--version", "sv3d_p",
            "--elevations_deg", elevations_str,
            "--azimuths_deg", azimuths_str
        ]
        subprocess.run(command)
        
        # Assuming the video is saved in the default output folder
        video_path = "outputs/simple_video_sample/sv3d_p/000000.mp4"
        if os.path.exists(video_path):
            st.session_state['final_video'] = video_path
            st.session_state['page'] = 3
            next_page(3)

# Page 3: Display final video
def page3():
    st.title("AI Image and Video Generator")
    st.title("Step 3: View and Download Video")

    if st.session_state.get('final_video'):
        st.video(st.session_state['final_video'])

        video_file = st.session_state['final_video']

        download_button_clicked = st.download_button(
            label="Download Video",
            data=open(video_file, "rb").read(),
            file_name=os.path.basename(video_file),
            mime="video/mp4"
        )

        if download_button_clicked:
            # Delete the video file after the download button is clicked
            delete_video_file(video_file)
            st.session_state.pop('final_video', None)

        if st.button("Generate Another Video", key="start_over"):
            delete_video_file(video_file)
            st.session_state['page'] = 1
            next_page(1)
    else:
        st.write("No video generated yet. Please go back and generate the video.")

# Function to delete the video file
def delete_video_file(filepath):
    try:
        os.remove(filepath)
    except OSError as e:
        st.error(f"Error: {e.strerror}")

# Navigation logic
if 'page' not in st.session_state:
    st.session_state['page'] = 1

if st.session_state['page'] == 1:
    page1()
elif st.session_state['page'] == 2:
    page2()
elif st.session_state['page'] == 3:
    page3()
