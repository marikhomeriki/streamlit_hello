import streamlit as st
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import asyncio
import aiohttp
import validators
from datetime import datetime
import numpy as np
import altair as alt
data = 0

backup_data = {"cnn_model": {
        "Negative": 1218,
        "Positive": 307
    }}

backup_absa = {
    "absa": {
        "Positive": {
            "service": 78,
            "food": 91,
            "staff": 35,
            "fries": 22,
            "manager": 8
        },
        "Negative": {
            "service": 190,
            "food": 130,
            "staff": 84,
            "fries": 56,
            "manager": 73
        },
        "Neutral": {
            "service": 7,
            "food": 44,
            "staff": 3,
            "fries": 13,
            "manager": 3
        }
    }
}

st.set_page_config(page_title="Product Review Analysis",
                   page_icon="tada",
                   layout="wide", )


#Async START
async def api_call(source, url, pages):
    # TODO: use environment variables
    API_URL_REMOTE = "https://pra-icpdyxu5pq-nw.a.run.app/analyze"
    API_URL_LOCAL = "http://localhost:8080/analyze"

    timeout = aiohttp.ClientTimeout(total=600)
    params = {'source': source, 'url': url, 'pages': pages}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(API_URL_REMOTE, params=params) as response:
            data = await response.json()
            st.session_state['data'] = data
            st.experimental_rerun()


#Async END

original_title = '<b style="text-align:center; color:black; font-size: 70px;">Product Review Analysis</b>'
st.markdown(original_title, unsafe_allow_html=True)

st.sidebar.markdown("# What is a Review Analysis?")
st.sidebar.markdown("Review analysis is the act of going through customer\
        and product reviews from a number of different channels and uncovering \
        insights. These insights can then be used to improve products and \
        services, create new ones, or enhance the overall customer experience.")
st.sidebar.write("---")
x = st.sidebar.slider('Rate this website:',0,5)
if x==1:
    st.sidebar.markdown("⭐")
if x==2:
    st.sidebar.markdown("⭐⭐")
if x==3:
    st.sidebar.markdown("⭐⭐⭐")
if x==4:
    st.sidebar.markdown("⭐⭐⭐⭐")
if x==5:
    st.sidebar.markdown("⭐⭐⭐⭐⭐")

y = st.sidebar.text_area("Feedback:",max_chars=250)
st.sidebar.write("---")
z = st.sidebar.button("Submit")
if x ==0 or y == '':
    st.sidebar.write("Have not filled out the review")
else:
    st.sidebar.write("Thanks for the feedback! It means nothing tho loooool!")


with st.container():
    left_col,mid_col,right_col = st.columns(3)
    with left_col:
        st.markdown("### By Mariami Khomeriki, Ankur Kaushal,        \
               Mathias Freisleben, Arun Appulingam")

    with right_col:
        # file = open("https://cdn.searchenginejournal.com/wp-content/uploads/2021/04/google-product-reviews-update-606f3672ab023.jpg", 'rb')
        # contents = file.read()
        # data_url = base64.b64encode(contents).decode('utf-8-sig')
        # file.close()
        # st.markdown(f'<img src="data:image/gif;base64,{data_url}">',unsafe_allow_html = True)
        st.image("https://cdn.searchenginejournal.com/wp-content/uploads/2021/04/google-product-reviews-update-606f3672ab023.jpg")

# with st.container():
#     left_col, mid_col, right_col = st.columns(3)
#     with left_col:
#         # st.header("By Mariami Khomeriki, Ankur Kaushal, Mathias Freisleben\
#         #     , Arun Appulingam")
#         st.write("By Mariami Khomeriki, Ankur Kaushal, Mathias Freisleben, Arun Appulingam")

tab1,tab2,tab3 = st.tabs(["Summary 📈","Running the Data 😮","Backup Data 🔙"])

with tab1:
    st.markdown('# Summary📈')
    st.write("Product Review Analysis uses live-users-reviews from 'Yelp' or 'Trustpilot'\
        websites to analyse topic distribution by sentiment of the reviews, \
            for businesses to make better decisions.")

with tab2:
    st.markdown("# Running the Data 😮")

    st.markdown("#### Step 1:")

    form = st.form("form", clear_on_submit=True)

    with form:
        p1,p2 = st.columns(2)
        with p1:
            source = st.radio("Choose review data source", ('Yelp', 'TrustPilot'))
        with p2:
            pages = st.slider("Number of Pages", 1, 20, 1, step=1)
        url = st.text_input("URL", placeholder="Enter URL here.")
        submit = form.form_submit_button("Submit Now")

        if submit:
            if not validators.url(url):
                st.error('Invalid URL', icon="🚨")

            elif source == "Yelp" and "yelp.co.uk" not in url:
                st.error('Not a Yelp file',icon="🚨")

            elif source == "TrustPilot" and "trustpilot.com" not in url:
                st.error('Not a Trustpilot file',icon="🚨")

            else:
                if source == "Yelp" and "yelp.co.uk" in url:
                    st.success(
                    'Success, getting analysis from Yelp (can take up to 5 min)',
                    icon="✅")

                elif source == "Trustpilot" and "trustpilot.com" in url:
                    st.success(
                    'Success, getting analysis from Trustpilot (can take up to 5 min)',
                    icon="✅")

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(api_call(source, url, pages))


    st.write('---')

    #Async get data START
    data = st.session_state.get('data', None)
    #Async get data END







    if data:
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.header("Total")
        #     total = data['review_count']
        #     st.write(total)

        # with col2:
        #     st.header("AVG")
        st.markdown("# Graphs and Review Data 📊")
        st.markdown("#### Negative vs. Positive Reviews")
        cnn_model = pd.DataFrame.from_dict(data['cnn_model'], orient='index')
        words = data['words']
        words2v_neg = pd.DataFrame.from_dict(data['words2v_neg'])
        words2v_pos = pd.DataFrame.from_dict(data['words2v_pos'])
        absa = pd.DataFrame.from_dict(data['absa'])


        st.bar_chart(cnn_model)


        wordcloud = WordCloud(background_color="#F5F6F8", stopwords = STOPWORDS).generate(words)

        # Display the generated image:
        st.markdown("#### Most used words")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        st.pyplot()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Negatively used words")
            # st.write(words2v_neg)
            # st.bar_chart(words2v_neg)
            words2v_neg.reset_index(inplace = True)
            words2v_neg.columns = ["Words", "Scores"]
            st.write(words2v_neg)
            st.altair_chart(alt.Chart(words2v_neg).mark_bar(color='red',
            ).encode(
            x='Words',
            y='Scores'))

        with c2:
            st.markdown("#### Positively used words")
            # st.write(words2v_pos)
            # st.bar_chart(words2v_pos)
            words2v_pos.reset_index(inplace = True)
            words2v_pos.columns = ["Words", "Scores"]
            st.write(words2v_pos)
            st.altair_chart(alt.Chart(words2v_pos).mark_bar(color='green',
            ).encode(
            x='Words',
            y='Scores'))


        st.write(absa)
        st.bar_chart(absa)

with tab3:
    backup_cnn_model = pd.DataFrame.from_dict(backup_data['cnn_model'], orient='index')
    bakcup_absa = pd.DataFrame.from_dict(backup_absa['absa'])
    st.bar_chart(backup_cnn_model)
    st.write(bakcup_absa)
    st.bar_chart(bakcup_absa)

    c1, c2, c3 = st.columns(3)
    with c2:
        csv = st.file_uploader("If data does not input, upload the CSV file")

        if csv is not None and csv.type == 'text/csv':
            df = pd.read_csv(csv)
            df = df.reset_index()
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
