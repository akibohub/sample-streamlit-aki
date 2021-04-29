import streamlit as st 
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


st.title('顔認識アプリ')

subscription_key = 'c54fb1b970d64ffdb8323ca3f6a17e35'
assert subscription_key

face_api_url = 'https://20210430akibo.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age, gender, headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion,accessories,blur,exposure,noise'    
    }
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()

    font_size = 24
    font_name = "C:\Windows\Fonts\meiryo.ttc"
    font = ImageFont.truetype(font_name, font_size)

    for result in results:    
        rect = result['faceRectangle']
        gender = result['faceAttributes']['gender']
        age = str(result['faceAttributes']['age'])
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=5)
        print(rect['left'])
        print(rect['top'])
        draw_x = rect['left'] - 25
        draw_y = rect['top'] - 30    
        draw.text((draw_x, draw_y), gender, font=font, fill=(255,0,0,128))    
        draw.text((draw_x + 80, draw_y), age, font=font, fill=(255,0,0,128))

    st.image(img, caption='Uploaded Image.', use_column_width=True)
