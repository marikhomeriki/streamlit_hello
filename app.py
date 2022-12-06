import streamlit as st
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import asyncio
import aiohttp
import validators
from datetime import datetime

st.set_page_config(page_title="Product Review Analysis",
                   page_icon="tada",
                   layout="wide")


#Async START
async def api_call(source, url, pages):
    # TODO: use environment variables
    API_URL_REMOTE = "https://pra-icpdyxu5pq-nw.a.run.app/analyze"
    API_URL_LOCAL = "http://localhost:8080/analyze"

    timeout = aiohttp.ClientTimeout(total=600)
    params = {'source': source, 'url': url, 'pages': pages}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(API_URL_LOCAL, params=params) as response:
            data = await response.json()
            st.session_state['data'] = data
            st.experimental_rerun()


#Async END

original_title = '<b style="font-family:serif; text-align:center; color:black; font-size: 70px;">Product Review Analysis</b>'
st.markdown(original_title, unsafe_allow_html=True)

with st.container():
    left_col, mid_col, right_col = st.columns(3)
    with left_col:
        st.header("By Mariami Khomeriki, Ankur Kaushal, Mathias Freisleben\
            , Arun Appulingam")

st.write("---")
st.markdown("# Introduction 📈")
st.sidebar.markdown("# Page 1: 📈")
st.header("Main Tasks")

st.write("This project is based around..........")

st.write("We divided the task in this were split within the group:")
st.write("Mari:")
st.write("Ankur:")
st.write("Mathias:")
st.write(
    "Arun: Creating a Sequential and CNN base model, helped clean data, using Streamline to make this website :)"
)

st.write("---")
st.markdown("# Running the Data 😮")
st.sidebar.markdown("# Page 2: 😮")

st.markdown("#### Step 1:")

form = st.form("form", clear_on_submit=True)

with form:
    source = st.radio("Choose review data source", ('Yelp', 'TrustPilot'))
    url = st.text_input("URL")
    pages = st.slider("Number of Pages", 1, 10, 1, step=1)
    submit = form.form_submit_button("Submit Now")

    if submit:
        if not validators.url(url):
            st.error('Invalid URL', icon="🚨")
        else:
            st.success(
                'Success, please wait for the data to process (can take up to 5 min)',
                icon="✅")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(api_call(source, url, pages))

st.write('---')

st.markdown("#### Step 3:")

c1, c2, c3 = st.columns(3)
with c2:
    csv = st.file_uploader("If data does not input, upload the CSV file")

    if csv is not None and csv.type == 'text/csv':
        df = pd.read_csv(csv)
        st.write(df)
    elif csv is not None and csv.type != 'text/csv':
        st.write('Not a CSV file')

    button_style = """
         <style>
        .stButton > button {
            color:black;
            text-align:center;
            width:200px;
            height:55px;
            }
        </style>
        """

st.markdown("# Graphs and Review Data 📊")
st.sidebar.markdown("# Page 3: 📊")

#Async get data START
data = st.session_state.get('data', None)
#Async get data END

if data:
    cnn_model = pd.DataFrame.from_dict(data['cnn_model'], orient='index')
    words = data['words']
    words2v_neg = pd.DataFrame.from_dict(data['words2v_neg'])
    words2v_pos = pd.DataFrame.from_dict(data['words2v_pos'])
    absa = pd.DataFrame.from_dict(data['absa'])

    st.bar_chart(cnn_model)

    wordcloud = WordCloud().generate(words)

    # Display the generated image:
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()

    c1, c2 = st.columns(2)
    with c1:
        st.write(words2v_neg)
        st.bar_chart(words2v_neg)
    with c2:
        st.write(words2v_pos)
        st.bar_chart(words2v_pos)

    st.write(absa)
    st.bar_chart(absa)
