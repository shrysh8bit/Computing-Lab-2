import operator

import a1_worldNews_2019 
import a2_worldNews_2020_jan 
import a2_worldNews_2020_feb_on 
import a3_world_response
import b1_country_argentina
import b1_country_australia_2020
import b1_country_australia_2021
import b1_country_australia_2022
import b1_country_bangladesh
import b1_country_brazil
import b1_country_canada
import b1_country_ghana_2020
import b1_country_ghana_2021
import b1_country_india_19_April_May
import b1_country_india_21
import b1_country_india_April_20
import b1_country_india_jun_20

world_news = []
world_response = []

data_list_names = [a1_worldNews_2019.date_news_2019, a2_worldNews_2020_jan.date_news_2020_onwards,
                    a2_worldNews_2020_feb_on.date_news_2020_onwards, b1_country_argentina.date_news_country,
                    b1_country_australia_2020.date_news_country, b1_country_australia_2021.date_news_country,
                    b1_country_australia_2022.date_news_country, b1_country_bangladesh.date_news_country,
                    b1_country_brazil.date_news_country, b1_country_canada.date_news_country,
                    b1_country_ghana_2020.date_news_country, b1_country_ghana_2021.date_news_country,
                    b1_country_india_19_April_May.date_news_country, b1_country_india_21.date_news_country,
                    b1_country_india_April_20.date_news_country, b1_country_india_jun_20.date_news_country]

# data_list_names = [b1_country_argentina.date_news_country, b1_country_brazil.date_news_country,
#                     b1_country_bangladesh.date_news_country, b1_country_canada.date_news_country]
# data_list_names = [a1_worldNews_2019.date_news_2019, a2_worldNews_2020_jan.date_news_2020_onwards,
#                     a2_worldNews_2020_feb_on.date_news_2020_onwards]


for list in data_list_names:
    for class_instance in list:
        world_news.append(class_instance)


for class_instance in a3_world_response.date_response:
    world_response.append(class_instance)



world_news.sort(key=operator.attrgetter('day'))
world_news.sort(key=operator.attrgetter('month'))
world_news.sort(key=operator.attrgetter('year'))
world_news.sort(key=operator.attrgetter('country'))



world_response.sort(key=operator.attrgetter('day'))
world_response.sort(key=operator.attrgetter('month'))
world_response.sort(key=operator.attrgetter('year'))
world_response.sort(key=operator.attrgetter('country'))

# for item in world_news:
#     print(item.country, item.day, item.month, item.year)

# for item in world_response:
#     print(item.country, item.day, item.month, item.year)