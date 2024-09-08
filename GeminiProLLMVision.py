from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from st_img_pastebutton import paste
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def getGemeniResponse(input, image):
    if input!="":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Gemeni image chatbot")
st.header("Gemeni Pro Image Chatbot")
input=st.text_input("Input:", key="input")

#Upload image
uploadedFile = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Create a paste button for images
image_data = paste(label="Paste an image from clipboard", key="image_clipboard")

image = ""

if uploadedFile is not None:
    image = Image.open(uploadedFile)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    #image = uploadedFile.read()

if image_data:
    # Decode the base64 image data
    header, encoded = image_data.split(",", 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_data))

    # Display the image
    st.image(image, caption="Pasted Image", use_column_width=True)

    # Save the image
    #image.save("pasted_image.png")

    st.success("Image pasted and saved successfully!")

submit = st.button("Tell me about this image")

if submit:
    response = getGemeniResponse(input, image)
    st.subheader("Response: ")
    st.write(response)
