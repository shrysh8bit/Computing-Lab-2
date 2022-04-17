from consolidated_data import world_news, world_response
import common_functions
from datetime import date
import re

def commonWords(text_1, text_2):
    common = ''
    for word in text_1:
        if word in text_2:
            common += " " + word

    return common

def getNewsInRange(source, country, start_date, end_date):
    # Return only the news in a single txt variable
    
    start_dt_list = common_functions.dateStrToList(start_date)
    end_dt_list = common_functions.dateStrToList(end_date)

    start_date = date(start_dt_list[2], start_dt_list[1], start_dt_list[0])
    end_date = date(end_dt_list[2], end_dt_list[1], end_dt_list[0])

    news = ''
    data_source = [world_response, world_news]

    for response in data_source:

        for response_instance in response:
            item_date = date(response_instance.year, response_instance.month, response_instance.day)
            
            if start_date <= item_date and item_date <= end_date:
                news = news + " " + response_instance.news

    return news



def printTopKWords(k, source_str):
    source_str_cleaned = re.sub("\.|,|;", " ", source_str)

    words_dict = {}
    words_list = source_str_cleaned.split()

    for word in words_list:
        if word not in words_dict:
            words_dict[word] = 1
        else:
            words_dict[word] = words_dict[word] + 1


    c_w_list_tup = list(words_dict.items())
    c_w_list_list = [[item[1], item[0]] for item in c_w_list_tup ]
    c_w_list_list.sort(reverse = True)
    c_w_list_list = c_w_list_list[:k]
    

    for item in c_w_list_list:
        print (f'{item [1]} occures {item[0]} times ' )
    

def task1(start_date, stop_date):

    print(f'Printing word cloud for World News between {start_date} and {stop_date}')
    news_wordcloud = common_functions.getNewsInRangeForWordCLoud (world_news, 'World', start_date, stop_date)
    common_functions.printWordCloud(news_wordcloud, 'Word Cloud of World News for selected date range')


    print(f'Printing word cloud for World Response between {start_date} and {stop_date}')
    response_wordcloud = common_functions.getNewsInRangeForWordCLoud (world_response, 'World', start_date, stop_date)
    common_functions.printWordCloud(response_wordcloud, 'Word Cloud of World Response for selected date range')


    print(f'Printing news for World :')
    common_functions.printNews(world_news, 'World', start_date, stop_date)


    print(f'Printing response for World :')
    common_functions.printNews(world_response, 'World', start_date, stop_date)

    

def task2(first_start_date, first_stop_date, second_start_date, second_stop_date):
    first_news_wordcloud = common_functions.getNewsInRangeForWordCLoud (world_news, 'World', first_start_date, first_stop_date)
    second_news_wordcloud = common_functions.getNewsInRangeForWordCLoud (world_news, 'World', second_start_date, second_stop_date)

    first_news_tokens = common_functions.tokeniseAndRemoveStopWords(first_news_wordcloud)
    second_news_tokens = common_functions.tokeniseAndRemoveStopWords(second_news_wordcloud)

    print(f'The word cloud for all common words is being drawn')
    common_words = common_functions.commonWords(first_news_tokens, second_news_tokens)
    common_functions.printWordCloud(common_words, 'Word Cloud of Common Words')
    # print (" Combined news words", common_words)

    with open("covid_word_dictionary.txt", 'r') as covid_word_dictionary:
        covid_words = covid_word_dictionary.read()

    covid_words = covid_words.lower()
    covid_words_list = covid_words.split('\n')

    print (len(covid_words_list), len(first_news_tokens), len(second_news_tokens))
    first_news_covid_words = common_functions.commonWords(first_news_tokens, covid_words_list)
    combined_news_covid_words = common_functions.commonWords(second_news_tokens, first_news_covid_words)

    # print (len(covid_words_list), len(first_news_covid_words), len(combined_news_covid_words))

    print(f'The word cloud for all common Covid words is being drawn')
    # print (" Combined news covid words", combined_news_covid_words)
    common_functions.printWordCloud(combined_news_covid_words, 'Word Cloud of Common Words')

    covid_word_perc = (len(set(combined_news_covid_words.split())) * 100)/ len(set(common_words.split()))
    print(f'The percentage of covid words in common words is {round(covid_word_perc, 2)}%')

    print(" ")
    print(f'The top 20 common words along with their frequencies are :')
    printTopKWords(20, common_words)

    print(" ")
    print(f'The top 20 common covid words along with their frequencies are :')
    printTopKWords(20, combined_news_covid_words)


