import openai
import streamlit as st
from PIL import Image, ImageDraw
from io import BytesIO
import base64

# Set your API key
openai.api_key = "your_openai_api_key_here"

# Streamlit app title
st.title("Image Generation and Editing with OpenAI")

# Image creation
st.header("Image Creation")
image_description = st.text_input("Enter a description to generate an image:")

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

    response = openai.Image.create(**payload)
    generated_image_url = response["data"][0]["url"]
    st.image(generated_image_url, caption="Generated Image", width=300)
    st.markdown(get_image_download_link(generated_image_url, "generated_image.png", "Download generated image"), unsafe_allow_html=True)

# Image editing with mask
st.header("Image Editing with Mask")
uploaded_image = st.file_uploader("Upload an image for editing:")

def get_image_download_link(img_url, filename, text):
    img_data = requests.get(img_url).content
    b64 = base64.b64encode(img_data).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'

if uploaded_image is not None:
    original_image = Image.open(uploaded_image)
    st.image(original_image, caption="Original Image", width=300)

    mask_color = st.color_picker("Select a mask color:", value="#FF0000")
    x1 = st.number_input("Mask X1 position:", value=0)
    y1 = st.number_input("Mask Y1 position:", value=0)
    x2 = st.number_input("Mask X2 position:", value=100)
    y2 = st.number_input("Mask Y2 position:", value=100)

    if st.button("Edit Image with Mask"):
        # Create a copy of the original image to draw the mask
        image_with_mask = original_image.copy()
        draw = ImageDraw.Draw(image_with_mask)
        draw.rectangle([x1, y1, x2, y2], fill=mask_color)
        st.image(image_with_mask, caption="Image with Mask", width=300)

        # Convert the image with mask to base64
        buffered = BytesIO()
        image_with_mask.save(buffered, format="PNG")
        base64_encoded_image_with_mask = base64.b64encode(buffered.getvalue()).decode("utf-8")

        edit_description = st.text_input("Enter a description to edit the image with mask:")
        edit_payload = {
            "image": base64_encoded_image_with_mask,
            "description": edit_description,
            "model": "image-alpha-001",
        }

        edit_response = openai.Image.create_edit(**edit_payload)
        edited_image_url = edit_response["url"]

        st.image(edited_image_url, caption="Edited Image", width=300)
        st.markdown(get_image_download_link(edited_image_url, "edited_image_with_mask.png", "Download edited image with mask"), unsafe_allow_html=True),
# Request frequency limit
st.write("## Request Frequency Limit")
requests_per_minute = st.number_input("Enter maximum requests per minute:", min_value=1, value=10)
st.write("Limit your app to ", requests_per_minute, " requests per minute.")
