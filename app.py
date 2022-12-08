import streamlit as st
from transformers import AutoModelForQuestionAnswering,AutoTokenizer,pipeline
from caption import *
import requests
from bs4 import BeautifulSoup
import tensorflow as tf

@st.cache (allow_output_mutation=True)
def load_model():
    model1 = pipeline('question-answering', model='deepset/roberta-base-squad2', tokenizer='deepset/roberta-base-squad2')
    return model1
def load_image():
    img = st.file_uploader("Please upload the image", type=["jpg", "png", "jpeg"])
    return img
def show_image(img):
    st.image(img, use_column_width=True)
def caption_image(img):
    caption = caption_this_image(img)
    return caption

st.title("Ask questions based on your image or article")
m = load_model()
img = load_image()
if img is not None:
    show_image(img)
    caption = caption_this_image(img)
else:
    caption = ''
# st.write(caption)
st.write("OR")
articles = st.text_area("Please enter your article")
st.write("OR")
def get_link():
    link = st.text_area("Please enter the url of your article","https://www.example123.com")
    return link
link = get_link()
output = ''
def web_scraping(link):
    if link is not None:
        res = requests.get(link)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        output=''
        blacklist = [
            # '[document]',
            # 'noscript',
            # 'header',
            # 'html',
            # 'meta',
            # 'head', 
            # 'input',
            'script',
            "style"
        ]
        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
    return output
st.write(output)
output = web_scraping(link)
articles = articles + output + caption
quest = st.text_input("Ask your question")
button = st.button("Answer")

with st.spinner("Finding Answer..."):
    if button and articles:
        answers = m(question=quest, context=articles)
        st.success (answers ["answer"])