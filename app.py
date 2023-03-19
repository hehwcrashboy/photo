import requests
import io
import base64
from PIL import Image
import openai
import streamlit as st

# 设置API密钥
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 用于下载图像的函数
def get_image_download_link(img_data, filename, text):
    b64 = base64.b64encode(img_data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

# 显示生成的图像
def display_generated_image(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    st.image(img, caption="Generated Image", use_column_width=True)
    img_data = io.BytesIO()
    img.save(img_data, format="PNG")
    st.markdown(get_image_download_link(img_data.getvalue(), "generated_image.png", "Download generated image"), unsafe_allow_html=True)

# 标题和说明
st.title("Image Generation with OpenAI")
st.write("Enter a description and generate an image based on the description. You can also upload an image for editing.")

# 文本输入和文件上传
image_description = st.text_input("Image Description", "A beautiful sunset over the ocean")
uploaded_file = st.file_uploader("Upload an image for editing (optional)", type=["png", "jpg", "jpeg"])

editing_image = None
if uploaded_file is not None:
    editing_image = Image.open(uploaded_file)
    st.image(editing_image, caption="Uploaded Image", use_column_width=True)

# 生成图像按钮
if st.button("Generate Image"):
    st.markdown("Generating image...")

    prompt = image_description
    model = "image-alpha-001"
    payload = {
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": "256x256",
        "response_format": "url",
    }

    if editing_image is not None:
        img_bytes = io.BytesIO()
        editing_image.save(img_bytes, format="PNG")
        base64_encoded_img = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
        payload["input_image"] = f"data:image/png;base64,{base64_encoded_img}"

    response = openai.Image.create(**payload)
    generated_image_url = response["data"][0]["url"]
    display_generated_image(generated_image_url)
