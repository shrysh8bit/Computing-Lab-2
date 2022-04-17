# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def tokeniseAndRemoveStopWords(text_str):

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(example_sent)
    
    filtered_sentence = [word for word in word_tokens if word.lower() not in stop_words]
    # print(filtered_sentence)
    filtered_sentence = []
    
    for word in word_tokens:
        if word not in stop_words:
            filtered_sentence.append(word)


    # print(word_tokens)
    # print(filtered_sentence)
    return filtered_sentence

# example_sent = """This is a sample sentence,
#                   showing off the stop words filtration."""

# tokeniseAndRemoveStopWords(example_sent)