import openai
import streamlit as st
import requests
from PIL import Image
import io

openai.api_key = st.secrets["OPENAI_API_KEY"]

def create_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="512x512", model="image-alpha-001")
    return response['data'][0]['url']

def edit_image(image_url, prompt):
    response = openai.Image.create_edit(image_url=image_url, prompt=prompt, n=1, model="image-alpha-001")
    return response['data'][0]['url']

def create_variation(image_url, prompt):
    response = openai.Image.create_variation(image_url=image_url, prompt=prompt, n=1, model="image-alpha-001")
    return response['data'][0]['url']

def get_image_download_link(image_url, filename, text):
    img_data = requests.get(image_url).content
    b64 = base64.b64encode(img_data).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}" target="_blank">{text}</a>'

st.title("Image Generation and Editing with OpenAI")

# Image upload
uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)
    uploaded_image_url = f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}"

# Text prompt
prompt = st.text_input("Enter a description to generate or edit an image:")

if st.button("Generate Image"):
    if uploaded_file is not None:
        edited_image_url = edit_image(uploaded_image_url, prompt)
        st.image(edited_image_url, caption="Edited image", use_column_width=True)
        st.markdown(get_image_download_link(edited_image_url, "edited_image.png", "Download edited image"), unsafe_allow_html=True)
    else:
        generated_image_url = create_image(prompt)
        st.image(generated_image_url, caption="Generated image", use_column_width=True)
        st.markdown(get_image_download_link(generated_image_url, "generated_image.png", "Download generated image"), unsafe_allow_html=True)
