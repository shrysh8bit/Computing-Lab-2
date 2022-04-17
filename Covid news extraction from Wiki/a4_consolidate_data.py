import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from a1_worldNews_2019 import date_news_2019
from a2_worldNews_2020_jan import date_news_2020_onwards

date_news = []

for item in date_news_2019:
    date_news.append(item)

for item in date_news_2020_onwards:
    date_news.append(item)
    

date_news.sort(key=operator.attrgetter('day'))
date_news.sort(key=operator.attrgetter('month'))
date_news.sort(key=operator.attrgetter('year'))


text = date_news[0].news
print (text)
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# for item in date_news:   
#     print (item.day, item.month, item.year, item.news)