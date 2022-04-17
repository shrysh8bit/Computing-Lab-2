from consolidated_data import world_news
import common_functions
from datetime import date
# import re

# def commonWords(text_1, text_2):
#     common = ''
#     for word in text_1:
#         if word in text_2:
#             common += " " + word

#     return common

country_names = ['Canada', 'Brazil', 'Argentina', 'Bangladesh', 'Australia',
            'Ghana', 'India'  ]


# country = 'Canada'
# date_list = common_functions.dateRangeForNews(world_news, country)
# print (date_list[0], date_list[1])

# country = 'Brazil'
# date_list = common_functions.dateRangeForNews(world_news, country)
# print (date_list[0], date_list[1])

# ref_country = 'Argentina'

# start_date_str = '01-1-2020'
# end_date_str = '30-11-2022'

# ref_news = ''
# ref_country = 'Argentina'
# date_list = common_functions.dateRangeForNews(world_news, ref_country)
# print (date_list[0], date_list[1])
# ref_news = common_functions.getNewsInRangeForWordCLoud(world_news, ref_country, start_date_str, end_date_str)

# covid_words = common_functions.covidWordsStr()
# ref_news_covid = common_functions.commonWords(covid_words.split(), ref_news.split())
# print (f'Ref covid words len {len(ref_news_covid)}')
# date_range = common_functions.dateRangeForNews(world_news, country)
    
# start_date_str = '{:%d-%m-%Y}'.format(date_range[0])
# end_date_str = '{:%d-%m-%Y}'.format(date_range[1])
# # print(start_date_str, end_date_str)

# news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, end_date_str)

# def jaccardSimilarity(ref_text, sample_text):
#     ref_text_token = common_functions.tokeniseAndRemoveStopWords(ref_text)
#     sample_text_token = common_functions.tokeniseAndRemoveStopWords(sample_text)

#     ref_text_set = set(ref_text_token)
#     sample_text_set = set(sample_text_token)

#     print ("Len of set : ", len(ref_text_set), len(sample_text_set))

#     j_index = (len(ref_text_set.intersection(sample_text_set)))/(len(ref_text_set.union(sample_text_set)))
#     # print(j_index)
#     return j_index

def jaccard(country, start_date, stop_date):

    jaccard_dict = {}

    start_date_str = start_date.strftime('%d-%m-%Y')
    stop_date_str = stop_date.strftime('%d-%m-%Y')
    
    ref_news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, stop_date_str)

    for country in country_names:
        news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, stop_date_str)
        jaccard_dict[country] = common_functions.jaccardSimilarity(ref_news, news)


    print(f'\nSimilarity of news with top 3 countries')
    c_w_list_tup = list(jaccard_dict.items())
    c_w_list_list = [[item[1], item[0]] for item in c_w_list_tup ]
    c_w_list_list.sort(reverse = True)
    c_w_list_list = c_w_list_list[1:4]
    for item in c_w_list_list:
        print (f'{item[1]} has {round(item[0], 2)}% similarity')


def jaccardCovid(country, start_date, stop_date):

    jaccard_covid_dict = {}

    with open("covid_word_dictionary.txt", 'r') as covid_word_dictionary:
        covid_words = covid_word_dictionary.read()

    covid_words = covid_words.lower()
    covid_words_list = covid_words.split('\n')

    start_date_str = start_date.strftime('%d-%m-%Y')
    stop_date_str = stop_date.strftime('%d-%m-%Y')
    
    ref_news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, stop_date_str)
    ref_covid_news = common_functions.commonWords(ref_news.split(), covid_words_list)

    for country in country_names:
        news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, stop_date_str)
        covid_news = common_functions.commonWords(news.split(), covid_words_list)
        jaccard_covid_dict[country] = common_functions.jaccardSimilarity(ref_covid_news, covid_news)


    print(f'\nSimilarity of Covid news with top 3 countries')
    c_w_list_tup = list(jaccard_covid_dict.items())
    c_w_list_list = [[item[1], item[0]] for item in c_w_list_tup ]
    c_w_list_list.sort(reverse = True)
    c_w_list_list = c_w_list_list[1:4]
    for item in c_w_list_list:
        print (f'{item[1]} has {round(item[0], 2)}% similarity')

    # print(" ")
    # print(f'Similarity of Covid news with all countries')

    # # print (len(covid_words), covid_words)

    # for country in country_names:
    #     news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, end_date_str)
    #     news_covid = common_functions.commonWords(covid_words.split(), news.split())
    #     jaccard_covid_dict[country] = common_functions.jaccardSimilarity(ref_news_covid, news_covid)

    # for key,val in jaccard_covid_dict.items():
    #     print (key, val)





# country = 'Canada'
# news_1 = common_functions.getNewsInRangeForWordCLoud (world_news, country, '01-10-2020', '30-11-2022')
# # common_functions.printWordCloud(news_1)
# common_functions.printNews(world_news, country, '01-10-2019', '28-2-2021' )



# news_2 = getNewsInRange ('01-1-2021', '28-2-2021')


# news_1_tokens = common_functions.tokeniseAndRemoveStopWords(news_1)
# news_2_tokens = common_functions.tokeniseAndRemoveStopWords(news_2)

# # print(len(news_1), type(news_1), news_1_tokens)
# # print(len(news_2), type(news_2), news_2_tokens)

# common_words = commonWords(news_1_tokens, news_2_tokens)
# # print(len(common_words), type(common_words), common_words)

# common_functions.printWordCloud(common_words)

# with open("covid_word_dictionary.txt", 'r') as covid_word_dictionary:
#     covid_words = covid_word_dictionary.read()

# covid_words = covid_words.lower()
# covid_words_list = covid_words.split('\n')

# combined_tokens = []

# for word in news_1_tokens:
#     combined_tokens.append(word)

# for word in news_2_tokens:
#     combined_tokens.append(word)

# covid_common_words = commonWords(news_1_tokens, covid_words_list)
# # print(len(covid_common_words), type(covid_common_words), covid_common_words)
# common_functions.printWordCloud(covid_common_words)

# covid_word_perc = (len(covid_common_words) * 100)/ len(common_words)
# print(f'The percentae of covid words in common words is {round(covid_word_perc, 2)}')


# def top20Words(list_of_words):
#     list_of_words = re.sub("\.|,|;", " ", list_of_words)
#     # print(list_of_words)
#     words_dict = {}
#     words_list = list_of_words.split()

#     for word in words_list:
#         if word not in words_dict:
#             words_dict[word] = 1
#         else:
#             words_dict[word] = words_dict[word] + 1


#     c_w_list_tup = list(words_dict.items())
#     c_w_list_list = [[item[1], item[0]] for item in c_w_list_tup ]
#     c_w_list_list.sort(reverse = True)
#     c_w_list_list = c_w_list_list[:20]
    
#     # for key, value in common_word_dict.items():
#     #     print (key, value)
    
#     c_w_20_dict = dict(c_w_list_list)

#     return c_w_20_dict



# common_word_dict = {}
# covid_word_dict = {}

# common_word_dict = top20Words(common_words)
# covid_word_dict = top20Words(covid_common_words)

# print(f'The top 20 common words in the date range are :')
# for key,val in common_word_dict.items():
#     print (key, val)

# print(f'The top 20 common covid words in the date range are :')

# for key,val in covid_word_dict.items():
#     print (key, val)


