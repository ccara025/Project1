import streamlit as st
import numpy as np
import pandas as pd
#Carlos Caraballo



import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("COP 4813 - Project 1")
#Part 1
st.write("Part 1 - Top Stories API")

name = st.text_input("Please enter your name here")

option = st.selectbox(
    "Please select your favorite topic",
    ["arts", "automobiles", "books", "business", "fashion",
     "food", "health", "home", "insider", "magazine", "movies",
     "nyregion", "obituaries", "opinion", "politics",
     "realestate", "science", "sports", "sundayreview",
     "technology", "theater", "t-magazine", "travel",
     "upshot", "us", "world"]
)
name.capitalize() + ', you selected :', option + '.'


api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]


url = "https://api.nytimes.com/svc/topstories/v2/" + option + ".json?api-key=" + api_key
response = requests.get(url).json()

main_functions.save_to_file(response,"JSON_Files/response.json")
my_articles = main_functions.read_from_file("JSON_Files/response.json")

str1 = ""
for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

sentences = sent_tokenize(str1)
words = word_tokenize(str1)

fdist = FreqDist(words)

words_no_punc = []

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())


fdist2 = FreqDist(words_no_punc)
stopwords = stopwords.words("english")

clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)


fdist3 = FreqDist(clean_words)
mostcommon = fdist3.most_common(10)
wordcloud = WordCloud().generate(str1)


chart_data = pd.DataFrame(
    mostcommon,
    mostcommon
)



plt.figure(figsize=(20,20))
plt.imshow(wordcloud)
plt.axis("off")


if st.checkbox("Click here for frequency distribution") :
    st.write("These are 10 most common words in the top stories of the topic you "
         "selected and the amount of times they appear:")
    st.line_chart(chart_data)

#will save plot as image and display it in streamlit
#source Stackoverflow
if st.checkbox("Click here to generate wordcloud"):
    wordcloud.to_file('JSON_Files/wordcloud.png')
    st.image('JSON_Files/wordcloud.png')


#Part B
st.write("Part B - Most Popular Articles")
option2 = st.selectbox(
    "Select your preferred set of articles" ,
    ["shared", "emailed", "viewed"]
)
'You selected :', option2

option3 = st.selectbox(
     "What amount of time do you want the articles from (in days) ?",
    ["1", "7", "30"]
)
'You selected :', option3

#second url look up but for popular articles
url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + option3 + ".json?api-key=" + api_key
response2 = requests.get(url2).json()

main_functions.save_to_file(response2,"JSON_Files/response2.json")
my_articles2 = main_functions.read_from_file("JSON_Files/response2.json")

str2 = ""
for i in my_articles2["results"]:
    str2 = str2 + i["abstract"]

sentences2 = sent_tokenize(str2) #will write words into sentences
words2 = word_tokenize(str2) #will list words one by one

wordcloud2 = WordCloud().generate(str2)

plt.figure(figsize=(10,12))
plt.imshow(wordcloud2)

plt.axis("off")


#will save plot as image and display it in streamlit
#source Stackoverflow
wordcloud2.to_file('JSON_Files/wordcloud2.png')
st.image('JSON_Files/wordcloud2.png')




