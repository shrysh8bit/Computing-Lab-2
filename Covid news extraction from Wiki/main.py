from consolidated_data import world_news, world_response
import task1_world
import common_functions
from datetime import date
import country_task
import os
from main_assgn4 import *
# import re

def inputDateValidity(date):
    if '-' not in date:
        return False
    
    date_list = date.split('-')

    if not date_list[0].isnumeric() or not date_list[1].isnumeric() or not date_list[2].isnumeric():
        return False
    
    # print (f' Returning {date} as True')
    return True


def inputDatePair():
    print ("Enter start date in format dd-mm-yyyy")
    start_date_str = input()

    if not inputDateValidity(start_date_str):
        print(f'Invalid date entered, Please choose again')
        print(f'Press enter to continue')
        temp = input()
        worldMenu()

    print ("Enter stop date in format dd-mm-yyyy")
    stop_date_str = input()

    if not inputDateValidity(stop_date_str):
        print(f'Invalid date entered, Please choose again')
        print(f'Press enter to continue')
        temp = input()
        worldMenu()

    start_date_list = common_functions.dateStrToList(start_date_str)
    stop_date_list = common_functions.dateStrToList(stop_date_str)

    try:
        date_1 = date(start_date_list[2], start_date_list[1], start_date_list[0])
        date_2 = date(stop_date_list[2], stop_date_list[1], stop_date_list[0])
        
    except:
        print("Invalid date(s) entered")
        print(f'Press enter to continue')
        temp = input()
        worldMenu()

    if date_1 > date_2:
        print ("Start date greater than stop date")
        print(f'Press enter to continue')
        temp = input()
        worldMenu()

    dates = []
    dates.append(date_1)
    dates.append(date_2)

    return dates


choice_cat = ['World', 'Country']

def printHelp():
    print('\n')
    print("Please enter 'World' to see world news and response for a selected date range.")
    print("Please enter the name of any of the following continents to get data for them. The names are:")
    [print(country+"  ") for country in country_names]
    # print("Please enter the name of any of the following countries to get data for them. The names are:")
    # [print(country_name+"  ") for country_name in countries_list]
    # print("Please type exit to terminate the program.")
    print("Thank you for using, and I hope the above inputs were helpful. Press enter to go back to the main menu")
    input()
    return mainMenu()

def worldMenu():

    os.system('clear')
    print ("welcome to the World menu of Covid Worldometer Program")
    print ("Please select choice of date range ")
    print ("Single date range -> 1 (Task 1)")
    print ("Double date range -> 2 (Task 2)")
    choice = input()
    print(" ")

    if choice != '1':
        if choice != '2':
            print(f'Invalid choice enetered, Please choose again')
            print(f'Press enter to continue')
            temp = input()
            worldMenu()
    
    # if choice == '1':
    #     date_pair_1 = inputDatePair()

    #     worldMenu()
    
    if choice == '1':
        date_pair_1 = inputDatePair()

        date1_str = date_pair_1[0].strftime('%d-%m-%Y')
        date2_str = date_pair_1[1].strftime('%d-%m-%Y')

        task1_world.task1(date1_str, date2_str)

        print(f'Press enter to continue')
        temp = input()
        mainMenu()

    if choice == '2':

        date_pair_1 = inputDatePair()

        print("Enter dates for second date range")
        date_pair_2 = inputDatePair()

        first_start_date = date_pair_1[0].strftime('%d-%m-%Y')
        first_stop_date = date_pair_1[1].strftime('%d-%m-%Y')
        second_start_date = date_pair_2[0].strftime('%d-%m-%Y')
        second_stop_date = date_pair_2[1].strftime('%d-%m-%Y')


        if date_pair_1[0] > date_pair_2[0] or date_pair_1[0] > date_pair_2[1]:
            print("Dates overlapping or not in sequence")
            print(f'Press enter to continue')
            temp = input()
            return worldMenu()

        if date_pair_1[1] > date_pair_2[0] or date_pair_1[1] > date_pair_2[1]:
            print("Dates overlapping or not in sequence")
            print(f'Press enter to continue')
            temp = input()
            return worldMenu()


        task1_world.task2(first_start_date, first_stop_date, second_start_date, second_stop_date)

        print(f'Press enter to continue')
        temp = input()
        mainMenu()


country_names = ['Canada', 'Brazil', 'Argentina', 'Bangladesh', 'Australia',
            'Ghana', 'India'  ]


def countryMenu():

    os.system('clear')
    print ("welcome to the Country menu of Covid Worldometer Program")
    print ("Please enter choice of country ")
    print("Enter 'help' to see the list of countries")
    choice = input()
    
    if choice == 'help':
        for name in country_names:
            print (name)
        
        print(f'Press enter to continue')
        temp = input()
        countryMenu()

    if choice not in country_names:
        print(f'Invalid country name enetered, Please choose again')
        print(f'Press enter to continue')
        temp = input()
        countryMenu()
    # print(" ")

    date_list = common_functions.dateRangeForNews(world_news, choice)
    print(f'The news for {choice} is available from {date_list[0]} to {date_list[1]}')

    print("\nEnter the date range for which you wish to check the news, a word cloud and nearest 3 similar countries")
    date_pair_1 = inputDatePair()

    start_date_str = date_pair_1[0].strftime('%d-%m-%Y')
    stop_date_str = date_pair_1[1].strftime('%d-%m-%Y')
    
    common_functions.printNews(world_news, choice, start_date_str, stop_date_str)

    news_wordcloud_str = common_functions.getNewsInRangeForWordCLoud(world_news, choice,  start_date_str, stop_date_str)
    
    print(f'\nPrinting word cloud for {choice} for dates between {date_pair_1[0].day} {date_pair_1[0].month} {date_pair_1[0].year} to {date_pair_1[1].day} {date_pair_1[1].month} {date_pair_1[1].year}')
    common_functions.printWordCloud(news_wordcloud_str, 'Word Cloud for selected Country news')

    country_task.jaccard(choice, date_list[0], date_list[1])
    country_task.jaccardCovid(choice, date_list[0], date_list[1])

    print(f'Press enter to continue')
    temp = input()
    mainMenu()
    # print ("Single date range -> 1 (Task 1)")
    # print ("Double date range -> 2 (Task 2)")Country





def mainMenu():
    os.system('clear')
    print("Welcome to the Covid Worldometer Program")
    print("Please select a data category:")
    print (f"World data -> 'World' (Task 1 & 2)")
    print (f"Country data -> 'Country' (Task 3 - 6)")
    print(f"Historical & Yesterday data -> 'A4' (Assignment 4)")
    selection = input()

    if selection == 'World':
        worldMenu()
        mainMenu()
    if selection == 'Country':
        countryMenu()
        mainMenu()

    if selection == 'A4':
        menuInit()
        mainMenu()

    if selection == 'Help':
        printHelp()
        mainMenu()

    if selection not in choice_cat:
        print(f'Invalid choice enetered, Please choose again')
        print(f'Press enter to continue')
        temp = input()
        mainMenu()

mainMenu()
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







# jaccard_dict = {}
# jaccard_covid_dict = {}

# for country in country_names:
#     news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, end_date_str)
#     jaccard_dict[country] = common_functions.jaccardSimilarity(ref_news, news)


# print(f'Similarity of news with all countries')
# for key,val in jaccard_dict.items():
#     print (key, val)

# print(" ")
# print(f'Similarity of Covid news with all countries')

# # print (len(covid_words), covid_words)

# for country in country_names:
#     news = common_functions.getNewsInRangeForWordCLoud(world_news, country, start_date_str, end_date_str)
#     news_covid = common_functions.commonWords(covid_words.split(), news.split())
#     jaccard_covid_dict[country] = common_functions.jaccardSimilarity(ref_news_covid, news_covid)

# for key,val in jaccard_covid_dict.items():
#     print (key, val)
# # country = 'Canada'
# # news_1 = common_functions.getNewsInRangeForWordCLoud (world_news, country, '01-10-2020', '30-11-2022')
# # # common_functions.printWordCloud(news_1)
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


