import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from datetime import date

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def dateStrToList(date_str):
    # dt should be in format dd-mm-yyyy

    dd_mm_yyyy_list = date_str.split('-')
    dd_mm_yyyy_list = [int(x) for x in dd_mm_yyyy_list   ]
    return dd_mm_yyyy_list


def printWordCloud(text, heading):
    if len(text) <= 1:
        print("Insufficient data to print wordcloud")
        print("Please select alternate dates")
        return 

    wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)# Plot
    
    plt.figure(figsize=(50, 50))
    plt.title(heading)
    plt.imshow(wordcloud) 
    plt.axis("off");
    plt.show()    



def dateRangeForNews(news, name):
    # Returns the date range of news avail for a country name
    # in the news source provided

    # print("in date range for news")

    for instance in news:
        # print(instance.country, instance.year, instance.month, instance.day)    
        if instance.country == name:
            start_date = date(instance.year, instance.month, instance.day)    
            break
    # print("in date range for news, start_date", start_date)

    for instance in reversed(news):
        if instance.country == name:
            stop_date = date(instance.year, instance.month, instance.day)
            # print(instance.country, instance.year, instance.month, instance.day)    
            break
    # print("in date range for news, start_date, stop date", start_date, stop_date)

    dates = []
    dates.append(start_date)
    dates.append(stop_date)

    return dates



def getNewsInRangeForWordCLoud(news_source, country, start_date, end_date):
    # Return only the news in a single txt variable for plotting word cloud
    
    start_dt_list = dateStrToList(start_date)
    end_dt_list = dateStrToList(end_date)

    start_date = date(start_dt_list[2], start_dt_list[1], start_dt_list[0])
    end_date = date(end_dt_list[2], end_dt_list[1], end_dt_list[0])

    news = ''

    # print(start_date, end_date, len(news_source))

    for response in news_source:
        if response.country == country:
            # print(response.country, response.year)
            item_date = date(response.year, response.month, response.day)
            
            if start_date <= item_date and item_date <= end_date:
                news = news + " " + response.news
                # print(len(news))

    return news


def printNews(source, country, start_date, end_date):
    # Print the news for a country in a given date range
    print(f'\nThe news for {country} from {start_date} to {end_date} is given below:')
    start_dt_list = dateStrToList(start_date)
    end_dt_list = dateStrToList(end_date)

    start_date = date(start_dt_list[2], start_dt_list[1], start_dt_list[0])
    end_date = date(end_dt_list[2], end_dt_list[1], end_dt_list[0])

    for response in source:
        if response.country == country:
            item_date = date(response.year, response.month, response.day)
            
            if start_date <= item_date and item_date <= end_date:
                print (response.country, response.day, response.month, response.year)
                print (response.news)
                print (" ")


def covidWordsStr():
    with open("covid_word_dictionary.txt", 'r') as covid_word_dictionary:
        covid_words = covid_word_dictionary.read()

    covid_words = covid_words.lower()
    covid_words_list = covid_words.split('\n')
    
    words = ''
    for word in covid_words_list:
        words += " " + word

    return words

def commonWords(text_1, text_2):
    common = ''
    for word in text_1:
        if word in text_2:
            common += " " + word

    return common

# def newsAndWordCloud(start_date, end_date):
    
#     start_dt_list = dateStrToList(start_date)
#     end_dt_list = dateStrToList(end_date)

#     start_date = date(start_dt_list[2], start_dt_list[1], start_dt_list[0])
#     end_date = date(end_dt_list[2], end_dt_list[1], end_dt_list[0])

#     print(f'World news followed by world responses for ')
#     print(f'dates {start_date} to {end_date} are')
#     print(" ")

#     # country = 'World'
#     data_source = [world_response, world_news]

#     for response in data_source:
#         text_wordcloud = ''
#         news_to_show = []

#         for response_instance in response:
#             item_date = date(response_instance.year, response_instance.month, response_instance.day)
            
#             if start_date <= item_date and item_date <= end_date:
#                 text_wordcloud = text_wordcloud + " " + response_instance.news
#                 news_to_show.append(response_instance)

#         for item in news_to_show:
#             print(item.day, item.month, item.year, item.news)
#             print(" ")
    
#         printWordCloud(text_wordcloud)


def jaccardSimilarity(ref_text, sample_text):

    ref_text_token = tokeniseAndRemoveStopWords(ref_text)
    sample_text_token = tokeniseAndRemoveStopWords(sample_text)

    ref_text_set = set(ref_text_token)
    sample_text_set = set(sample_text_token)

    # print ("Len of set : ", len(ref_text_set), len(sample_text_set))

    j_index = (len(ref_text_set.intersection(sample_text_set)))/(len(ref_text_set.union(sample_text_set)))
    # print(j_index)
    return j_index
        


def tokeniseAndRemoveStopWords(text_str):
    # Tokenise non stopwords and return them as a list

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text_str)
    
    filtered_sentence = [word for word in word_tokens if word.lower() not in stop_words]
    # print(filtered_sentence)
    filtered_sentence = []
    
    for word in word_tokens:
        if word not in stop_words:
            filtered_sentence.append(word)


    # print(word_tokens)
    # print(filtered_sentence)
    return filtered_sentence

