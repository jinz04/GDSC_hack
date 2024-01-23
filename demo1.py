from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')


st.set_page_config("Skin disease predictor") 

def get_gemini_response(input,image_data,user_prompt):
    response = model.generate_content([input,image_data[0],user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts= [{
            'mime_type': uploaded_file.type,
            'data': bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')
 
   
st.header('Online Diagnostic System')
input = st.text_input('Input Prompt',key='input')
uploaded_file = st.file_uploader('Image',type=['jpg','jpeg','png'])
if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image,caption='Uploaded File',use_column_width=True)
    
sub = st.button('Predict the disease')    
    
input_prompt = """You are an expert in making medical diagnostics. You have to identify skin diseases from uploaded image and suggest treatment.
We will upload an image of disease symptoms or prescription and you will have to answer any question based on the uploaded image.
You have to specify the possible disease and treatment options available. You will also suggest ways to prevent the disease."""

if sub:
    with st.spinner('Wait'):
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data,input)
        st.subheader('Possible disease and its treatment is:')
        st.text_area(label="Response", value=response,height=500)
        
