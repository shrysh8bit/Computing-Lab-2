# from consolidated_data import world_response
from consolidated_data import world_news, world_response


import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from datetime import date

def dateStrToList(date_str):
    dd_mm_yyyy_list = date_str.split('-')
    dd_mm_yyyy_list = [int(x) for x in dd_mm_yyyy_list   ]
    return dd_mm_yyyy_list

def printWordCloud(text):

    wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)# Plot
    
    plt.figure(figsize=(50, 50))
    plt.imshow(wordcloud) 
    plt.axis("off");
    plt.show()    



def newsAndWordCloud(start_date, end_date):
    
    start_dt_list = dateStrToList(start_date)
    end_dt_list = dateStrToList(end_date)

    start_date = date(start_dt_list[2], start_dt_list[1], start_dt_list[0])
    end_date = date(end_dt_list[2], end_dt_list[1], end_dt_list[0])

    print(f'World news followed by world responses for ')
    print(f'dates {start_date} to {end_date} are')
    print(" ")

    # country = 'World'
    data_source = [world_response, world_news]

    for response in data_source:
        text_wordcloud = ''
        news_to_show = []

        for response_instance in response:
            item_date = date(response_instance.year, response_instance.month, response_instance.day)
            
            if start_date <= item_date and item_date <= end_date:
                text_wordcloud = text_wordcloud + " " + response_instance.news
                news_to_show.append(response_instance)

        for item in news_to_show:
            print(item.day, item.month, item.year, item.news)
            print(" ")
    
        printWordCloud(text_wordcloud)

        


newsAndWordCloud('01-1-2021', '28-2-2021')
