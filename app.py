import streamlit as st
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import asyncio
import aiohttp
from datetime import datetime

st.set_page_config(page_title="Product Review Analysis", page_icon= "tada", layout= "wide")

#Async START
async def api_call():
    # TODO: use environment variables
    API_URL_REMOTE = "https://pra-icpdyxu5pq-nw.a.run.app/analyze"
    API_URL_LOCAL = "http://localhost:8080/mock-analyze"

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(API_URL_REMOTE) as response:
            data = await response.json()
            st.session_state['data'] = data
            st.experimental_rerun()
#Async END


if st.button('Load'):
    # Run api call asynchronously not to block streamlit
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(api_call())


original_title = '<b style="font-family:serif; text-align:center; color:black; font-size: 70px;">Product Review Analysis</b>'
st.markdown(original_title, unsafe_allow_html=True)


with st.container():
    left_col,mid_col,right_col = st.columns(3)
    with left_col:
        st.header("By Mariami Khomeriki, Ankur Kaushal, Mathias Freisleben\
            , Arun Appulingam")




st.write("---")
st.markdown("# Introduction 📈")
st.sidebar.markdown("# Page 1: 📈")
st.header("Main Tasks")

st.write("This project is based around..........")

st.write("We divided the task in this were split within the group:")
st.write ("Mari:")
st.write ("Ankur:")
st.write ("Mathias:")
st.write ("Arun: Creating a Sequential and CNN base model, helped clean data, using Streamline to make this website :)")

st.write("---")
st.markdown("# Running the Data 😮")
st.sidebar.markdown("# Page 2: 😮")

st.markdown("#### Step 1:")

st.write("**`Get Review From :`**")

st.markdown("<h2 style='text-align: center;'>Choose One:</h2>",unsafe_allow_html= True)

column1,column2 = st.columns(2)

with column1:
    yelp = column1.checkbox('Yelp')

with column2:
    trust_pilot = column2.checkbox('TrustPilot')

st.info("**Choose an option using the boxes.**")
st.write('---')
st.markdown("### Step 2:")


form = st.form("form", clear_on_submit=True)
with form:
    url = st.text_input("**`Give the URL link:`**", None)


    number_of_pages = st.slider("**`Number of Pages:`**", 0, 40, 2, step=1)

    st.markdown("<h2 style='text-align: center;'>Choose One:</h2>",unsafe_allow_html= True)
    column1,column2 = form.columns(2)
    with column1:
        # st.image('/Users/arun._.appulingam/code/rsz_1googleimage.png')
        yelp = column1.checkbox('Yelp')

    with column2:
        # st.image('/Users/arun._.appulingam/code/rsz_1yelp-image.png')
        # column2.write(f"`Yelp`")
        trust_pilot = column2.checkbox('TrustPilot')


    flag = True
    if (url is not None) and ((not yelp and not trust_pilot)\
        or (yelp and not trust_pilot) or (not yelp and trust_pilot)):
        flag = True
    else:
        flag = False

    submit = form.form_submit_button("Submit Now")
    st.info("**Choose an option using the boxes.**")

    if submit:

        # check if url value is empty / if box is empty (or the default values)
        if url == "None" or url == '':
                    st.write("missing information, please fill out")
        # return the st.write that contains the intended message (i.e. please fill in missing info )
        elif 'https://www.yelp.' not in url:
                    st.write("this is not a Yelp file, please try again")
        else:
            output = get_data_yelp(url, pages = number_of_pages)
            st.write(yelp, output)
            st.balloons()


        # st.markdown("#### Step 2:")

        # check if url value is empty / if box is empty (or the default values)
        if url == "None" or url == '':
                    st.write("missing information, please fill out")
        # return the st.write that contains the intended message (i.e. please fill in missing info )
        elif 'https://www.yelp.' not in url:
                    st.write("this is not a Yelp file, please try again")
        else:
            output = get_data_yelp(url)
            st.write(yelp, output)
            st.balloons()


st.write('---')

st.markdown("#### Step 3:")

c1,c2,c3 = st.columns(3)
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

    c1,c2= st.columns(2)
    with c1:
        st.write(words2v_neg)
        st.bar_chart(words2v_neg)
    with c2:
        st.write(words2v_pos)
        st.bar_chart(words2v_pos)

    st.write(absa)
    st.bar_chart(absa)
