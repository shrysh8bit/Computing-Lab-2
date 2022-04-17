with open("covid_word_dictionary.txt", 'r') as covid_word_dictionary:
    covid_words = covid_word_dictionary.read()

# covid_words_list = [x.tolower() for x in covid_words_list]
# for word in covid_words:
covid_words = covid_words.lower()
covid_words_list = covid_words.split('\n')

print(covid_words_list)
