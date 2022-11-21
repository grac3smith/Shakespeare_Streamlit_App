import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
import nltk
nltk.download('punkt')
import altair as alt
from collections import Counter


st.write('# Analyzing Shakespeare Texts')

st.sidebar.header("Word Cloud Settings")
max_word = st.sidebar.slider("Max Words",10,200,100,10) #if you go in order you don't have to put label= etc.
max_font = st.sidebar.slider("Size of Largest Word",50,350,60) #size of font in word cloud
image_size = st.sidebar.slider("Image Width",100,800,400,10)
random = st.sidebar.slider("Random State",30,100,42)
use_stopwords = st.sidebar.checkbox('Remove Stop Words')

st.sidebar.header("Word Count Settings")
min_word = st.sidebar.slider("Minimum Count of Words", 5,100,40)

books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}
image = st.selectbox('Please select a Book', books.keys())
image=books.get(image)

if image != " ":
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])
    raw_text = open(image,"r").read().lower()
    #Remove punctuation
    dataset = re.sub(r'[^\w\s]', '', raw_text)

#Tokenize the dataset
    tokens = nltk.word_tokenize(dataset)
    tokens2 = [w for w in tokens if not w.lower() in stopwords] 
    word_count = Counter(tokens2)
    filtered_text = [w for w in tokens2 if not w.lower() in stopwords]
    f_counts = Counter(filtered_text)
    df = pd.DataFrame.from_dict(f_counts, orient='index').reset_index()
    df = df.rename(columns={'index':'Word', 0:'Count'})
    df2 = df.sort_values('Count', ascending=False).head(min_word)

#Create second dataset for bar graph with stopwords
    again_count = Counter(tokens)
    again_df = pd.DataFrame.from_dict(again_count, orient='index').reset_index()
    again_df = again_df.rename(columns = {'index':'Word', 0:'Count'})
    again_df2 = again_df.sort_values('Count', ascending = False).head(min_word)


tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    if use_stopwords:
        if image != " ":
            stopwords = set(STOPWORDS)
            stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
            'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
            'put', 'seem', 'asked', 'made', 'half', 'much',
            'certainly', 'might', 'came'])
            cloud = WordCloud(background_color = "white", 
            max_words = max_word, 
            max_font_size=max_font, 
            random_state=random,
            stopwords = stopwords)
            wc = cloud.generate(dataset)
            word_cloud = cloud.to_file('wordcloud.png') #not necessary for streamlit app to run. this just saves image to working directory
            st.image(wc.to_array(), width=image_size)            
            
    else:
        if image != " ":
            cloud = WordCloud(background_color = "white", 
            max_words = max_word, 
            max_font_size=max_font, 
            random_state=random)
            wc = cloud.generate(dataset)
            st.image(wc.to_array(), width=image_size)            

        


with tab2:
    if use_stopwords:
        if image != " ":
            bar1 = alt.Chart(df2, title='Word Counts Bar Graph').mark_bar().encode(
                x=alt.X('Word', sort='-y'),
                y='Count',
                color = alt.Color('Count', scale=alt.Scale(scheme='greens'), legend=None),
                tooltip = ['Word', 'Count']
            )
            st.altair_chart(bar1, use_container_width=True)
    else:
        if image != " ":
            bar2 = alt.Chart(again_df2, title='Word Counts Bar Graph').mark_bar().encode(
                x=alt.X('Word', sort='-y'),
                y='Count',
                color = alt.Color('Count', scale=alt.Scale(scheme='greens'), legend=None),
                tooltip = ['Word', 'Count']
            )
            st.altair_chart(bar2, use_container_width=True)      

with tab3:
    if image != " ":
        full_text = open(image,"r").read()
        st.write(full_text) #shows the whole play in tab 3
