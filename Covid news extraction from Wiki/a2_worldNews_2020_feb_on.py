import ply.lex as lex
import ply.yacc as yacc
import requests
import re


class newsItems:
    day = 0
    month = 0
    year = 0
    news = ''
    country = ''

date_news_2020_onwards = []

def splitInputStr(str, start_index, stop_index):
    count = 0
    for char in str:
        if char == '\n':
            count += 1

    rear_index = count - stop_index
    str_rear_split = str.rsplit('\n', rear_index)

    str = str_rear_split[0]
    str_front_split = str.split('\n', start_index)

    str = str_front_split[-1]
    return str

def cleanReadData(str_to_clean):
    re_str = re.sub("<.*?>|\d{0,3}&#\d{0,3};|citation\sneeded", "", str_to_clean)
    return re_str

def dateFormatting(month_fm_suffix, date_in_str):
    # print ("Incoming date in date format fn :", date_in_str, month_fm_suffix)
    date_in_str = date_in_str.lstrip('>').rstrip('<')
    dd_mm = date_in_str.split()

    date_list = [0]*3
    date_list[0] = int(dd_mm[0])
    
    month_fm_suffix_list = month_fm_suffix.split('_')
    
    month_str = dd_mm[1]
    # print (month_str, month_fm_suffix_list[0])
    if month_str != month_fm_suffix_list[0]:
        return [0,0,0]

    if month_str == 'January':
        date_list[1] = 1

    if month_str == 'February':
        date_list[1] = 2

    if month_str == 'March':
        date_list[1] = 3

    if month_str == 'April':
        date_list[1] = 4

    if month_str == 'May':
        date_list[1] = 5

    if month_str == 'June':
        date_list[1] = 6

    if month_str == 'July':
        date_list[1] = 7

    if month_str == 'August':
        date_list[1] = 8

    if month_str == 'September':
        date_list[1] = 9

    if month_str == 'October':
        date_list[1] = 10

    if month_str == 'November':
        date_list[1] = 11

    if month_str == 'December':
        date_list[1] = 12

    date_list[2] = int(month_fm_suffix_list[1])



    # print(date_list)
    return date_list


# str_date = '>1 December<'
# suffix = 'December 2020'
# dateFormatting(suffix, str_date)



def parseWorldWideNews():
    url_suffixes = [['February_2020',360, 810], ['March_2020',360, 1320], 
        ['April_2020', 360, 1240], ['May_2020', 360, 810], ['June_2020',360, 634], 
        ['July_2020', 360,773], ['August_2020', 360, 616], ['September_2020', 358, 570],
        ['October_2020',360, 590], ['November_2020', 360, 582], ['December_2020', 355, 616],
        ['January_2021', 355, 600], ['February_2021', 354, 556], ['March_2021', 354, 600], 
        ['April_2021', 355, 599], ['May_2021', 356, 620], ['June_2021', 355, 595], 
        ['July_2021', 355, 625], ['August_2021', 352, 665], ['September_2021', 353, 630], 
        ['October_2021',355,620], ['November_2021', 355, 612], ['December_2021', 355, 660],
        ['January_2022', 355, 770], ['February_2022', 352, 765], ['March_2022', 325, 450]]
    

    # url_suffixes = [['February_2020',360, 810], ['March_2020',360, 1320], 
    #     ['April_2020', 360, 1240], ['May_2020', 360, 810], ['June_2020',360, 634], 
    #     ['July_2020', 360,773], ['August_2020', 360, 616], ['September_2020', 358, 570]]

    for suffix in url_suffixes:

        base_url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_'
        url_to_call = base_url + suffix[0]
    
        html_data_raw = requests.get(url_to_call)
        html_data_str = (html_data_raw.text)
        html_data_str = splitInputStr(html_data_str, suffix[1], suffix[2])


        print (suffix, len(html_data_str))


        tokens = [  'BREAK', 'DATE', 'NEWS']
    
        def t_BREAK(t):
            r'<span.class=\"mw-headline\".id=\"\d'
            return t

        def t_DATE(t):
            r'>\d{1,2}.\w{3,10}<'
            return t

        def t_NEWS(t):
            r'(<li>.+</li>.*?\s*)+'
            return t

        def t_error (t):
            t.lexer.skip(1)
            return



        lexer = lex.lex()
        lexer.input(html_data_str)

        # while True:
        #     tok = lexer.token()
        #     if not tok:
        #         break
        #     print ("token : ", tok.type)

        # print("Lex Done")


    # ########################## End Of Lexer #########################################

        def p_start(t):
            '''start : news'''
                

        def p_news(t):
            '''news : DATE NEWS'''
            # print ("DATES1 : ", t[1]) 
            str_date = t[1]
            int_date_list = dateFormatting(suffix[0], str_date)
            news_instance = newsItems()
            news_instance.day = int_date_list[0]
            news_instance.month = int_date_list[1]
            news_instance.year = int_date_list[2]
            news_instance.news = cleanReadData(t[2])
            news_instance.country = 'World'

            # print (int_date_list)
            if news_instance.day != 0:
                global date_news_2020_onwards
                date_news_2020_onwards.append(news_instance)
            #     print("Date valid")
            # else:
            #     print("Date not valid")


        def p_error(p):
            pass
        
        parser = yacc.yacc()
        parser.parse(html_data_str)
        # print("Yacc Done")




parseWorldWideNews()    

# for item in date_news_2020_onwards:
#     print(item.day, item.month, item.year, item.news)



# print (date_news_2019[4].date, date_news_2019[4].news)

#  def p_total_cases(t):
#             'total_cases : TOTAL_CASES LINEAR_SCALE DATE_RANGE DATA'
#             # global main_data
#             # global countries_dict
#             dates = t[3]
#             new = dates[2:-2]
#             new = new.replace('","', ';')
#             new = new.split(";")
#             # main_data.append(new)

    #                 'DAILY_CASES', 'ACTIVE_CASES', 'DEATHS', 'BREAK', 'NEW_RECOVER']
    # list_of_country_data = []
    # for country_name in countries_list:
    #     print("Getting data for : ", country_name)
    #     url = "https://www.worldometers.info/coronavirus/country/" + country_name + "/"
    #     html_data = requests.get(url)
    #     html_data = str(html_data.content)
    #     print ("html data retrieved")

    #     country_data = ConsolidatedDataPerCountry()

    #     if country_name == 'US':
    #         country_name = 'USA'

    #     country_data.country_name = country_name
        # countries_dict[country_name] = html_data
    # print("Getting data for India")
    # url = "https://www.worldometers.info/coronavirus/country/india/"
    # html_data = requests.get(url)
    # html_data = str(html_data.content)
    # countries_dict["India"] = html_data
    # print (len(html_data), type(html_data))
    # print ( type(html_data))




#         tokens = [ 'TOTAL_CASES','LINEAR_SCALE', 'DATE_RANGE' , 'DATA',
#                 'DAILY_CASES', 'ACTIVE_CASES', 'DEATHS', 'BREAK', 'NEW_RECOVER']

#         def t_TOTAL_CASES(t):
#             r'Total\sCases'
#             return t

#         def t_LINEAR_SCALE(t):
#             r'Linear\sScale'
#             return t

#         def t_DATE_RANGE(t):
#             r'\[(,*\".{12}\")+\]'
#             return t

#         def t_DATA(t):
#             r'\[(null,)*\d+(,\d+)+\]'
#             return t

#         def t_ACTIVE_CASES(t):
#             r'>Active\sCases'
#             return t

#         def t_DAILY_CASES(t):
#             r'\'Daily\sCases'
#             return t

#         def t_DEATHS(t):
#             r'.Daily\sDeaths'
#             return t

#         def t_BREAK(t):
#             r'<style>'
#             return t

#         def t_NEW_RECOVER(t):
#             r'\'New\sRecoveries'
#             return t


#         t_ignore = " \t\n"

    


#         ###################### End Of Lexer #########################################


#         def p_start(t):
#             '''start : total_cases
#                     | daily
#                     | active
#                     | dead_ppl
#                     | new_recover'''



#         def p_total_cases(t):
#             'total_cases : TOTAL_CASES LINEAR_SCALE DATE_RANGE DATA'
#             # global main_data
#             # global countries_dict
#             dates = t[3]
#             new = dates[2:-2]
#             new = new.replace('","', ';')
#             new = new.split(";")
#             # main_data.append(new)
#             country_data.dates = new

#             cases = t[4]
#             new = cases[1:-1]
#             new = new.split(",")
#             new = [0 if x=='null' else x for x in new]
#             # main_data.append(new)
#             country_data.total_cases = new
#             print ("The dates for total cases are : ", t[1])


#         def p_daily(t):
#             'daily : DAILY_CASES DATA'
#             # global main_data
#             cases = t[2]
#             new = cases[1:-1]
#             new = new.split(",")
#             new = [0 if x=='null' else x for x in new]
#             # main_data.append(new)
#             country_data.daily_new_cases = new
#             print("In daily new cases", t[1])

#         def p_active(t):
#             'active : DEATHS ACTIVE_CASES DATE_RANGE DATA'
#             # global main_data
#             cases = t[4]
#             new = cases[1:-1]
#             new = new.split(",")
#             new = [0 if x=='null' else x for x in new]
#             # main_data.append(new)
#             country_data.active_cases = new
#             print ("In active cases")

#         def p_dead_ppl(t):
#             'dead_ppl : DEATHS DATA DATA DATA'
#             # global main_data
#             cases = t[2]
#             new = cases[1:-1]
#             new = new.split(",")
#             new = [0 if x=='null' else x for x in new]
#             # main_data.append(new)
#             country_data.daily_deaths = new
#             print("In daily deaths")

#         def p_new_recover(t):
#             'new_recover : NEW_RECOVER DATA'
#             # global main_data
#             cases = t[2]
#             new = cases[1:-1]
#             new = new.split(",")
#             new = [0 if x=='null' else x for x in new]
#             # main_data.append(new)
#             country_data.new_recoveries = new
#             print("In new Recoveries")

#         def p_error(p):
#             pass




#         parser = yacc.yacc()
#         parser.parse(html_data)
#         print("Yacc Done")

#         list_of_country_data.append(country_data)
#         print(country_data.country_name)
#         list_of_country_data = replaceEmptyListByZeroArray(list_of_country_data)

#         print ("xxxxxxxxxxxxxxxxxxxx End Of Parsing for : ", country_name)
#         print("\n\n")
#     return list_of_country_data


# # Fills PercentageChangeInData for a given country over the date range
# def getPercChangeOverDateRange(country_data, start_date, end_date):
#     start_date_data = extractDataForDate(country_data, start_date)
#     end_date_data = extractDataForDate(country_data, end_date)
#     if (start_date_data == None or end_date_data == None):
#         return None
#     return calcPercChangeInData(start_date_data, end_date_data, country_data.country_name)


# # For two given sets of data, calculate percentage change
# def calcPercChangeInData(start_data, end_data, country_name):
#     start_data = handleZeroesInData(start_data)
#     perc_change_in_data = PercentageChangeInData()
#     perc_change_in_data.country_name = country_name
#     perc_change_in_data.active_cases = (end_data.active_cases - start_data.active_cases)*100.0/start_data.active_cases
#     perc_change_in_data.daily_deaths = (end_data.daily_deaths - start_data.daily_deaths)*100.0/start_data.daily_deaths
#     perc_change_in_data.new_recovered = (end_data.new_recovered - start_data.new_recovered)*100.0/start_data.new_recovered
#     perc_change_in_data.new_cases = (end_data.new_cases - start_data.new_cases)*100.0/start_data.new_cases
#     return perc_change_in_data


# # replace 0 by 0.0001 to not break the percentage calculation
# def handleZeroesInData(data_for_date):
#     replacement_for_zero = 0.0001
#     if (data_for_date.active_cases == 0):
#         data_for_date.active_cases = replacement_for_zero
#     if (data_for_date.daily_deaths == 0):
#         data_for_date.daily_deaths = replacement_for_zero
#     if (data_for_date.new_recovered == 0):
#         data_for_date.new_recovered = replacement_for_zero
#     if (data_for_date.new_cases == 0):
#         data_for_date.new_cases = replacement_for_zero
#     return data_for_date


# # Return None if data not found for Date. Else extract all date for that date
# def extractDataForDate(country_data, date):
#     for index in range(0, len(country_data.dates)):
#         if (country_data.dates[index] == date):
#             data_for_date = DataPerDate()
#             data_for_date.date = date
#             data_for_date.active_cases = int(country_data.active_cases[index])
#             data_for_date.daily_deaths = int(country_data.daily_deaths[index])
#             data_for_date.new_recovered = int(country_data.new_recoveries[index])
#             data_for_date.new_cases = int(country_data.daily_new_cases[index])
#             return data_for_date
#     return None


# class ClosestCountries:
#     active_cases_country_name = 'dummy'
#     active_cases_perc = 99999999
#     daily_deaths_country_name = 'dummy'
#     daily_deaths_perc = 99999999
#     new_recovered_country_name = 'dummy'
#     new_recovered_perc = 99999999
#     new_cases_country_name = 'dummy'
#     new_cases_perc = 99999999


# def getClosestCountries(target_perc_change_in_data, list_of_all_country_data, start_date, end_date):
#     closest_countries = ClosestCountries()
#     for instance_of_country_data in list_of_all_country_data:
#         if (instance_of_country_data.country_name == target_perc_change_in_data.country_name):
#             continue
#         perc_change_in_data = getPercChangeOverDateRange(instance_of_country_data, start_date, end_date)
#         if (abs(closest_countries.active_cases_perc) > abs(target_perc_change_in_data.active_cases - perc_change_in_data.active_cases)):
#             closest_countries.active_cases_country_name = instance_of_country_data.country_name
#             closest_countries.active_cases_perc = perc_change_in_data.active_cases
#         if (abs(closest_countries.daily_deaths_perc) > abs(target_perc_change_in_data.daily_deaths - perc_change_in_data.daily_deaths)):
#             closest_countries.daily_deaths_country_name = instance_of_country_data.country_name
#             closest_countries.daily_deaths_perc = perc_change_in_data.daily_deaths
#         if (abs(closest_countries.new_recovered_perc) > abs(target_perc_change_in_data.new_recovered - perc_change_in_data.new_recovered)):
#             closest_countries.new_recovered_country_name = instance_of_country_data.country_name
#             closest_countries.new_recovered_perc = perc_change_in_data.new_recovered
#         if (abs(closest_countries.new_cases_perc) > abs(target_perc_change_in_data.new_cases - perc_change_in_data.new_cases)):
#             closest_countries.new_cases_country_name = instance_of_country_data.country_name
#             closest_countries.new_cases_perc = perc_change_in_data.new_cases
#     return closest_countries


# def sanityCheck(list_of_all_country_data):
#     for country_data in list_of_all_country_data:
#         print('country name is ', country_data.country_name)
#         print('len dates is ', len(country_data.dates), '  ', len(country_data.total_cases), ' ', len(country_data.daily_new_cases), '  ', len(country_data.active_cases), '  ', len(country_data.daily_deaths), '  ', len(country_data.new_recoveries))


# # When building country data, we get empty list if data is not present
# # This replaces that empty list by an array of zeroes
# def replaceEmptyListByZeroArray(list_of_all_country_data):
#     new_list_of_all_country_data = []
#     for country_data in list_of_all_country_data:
#         len_dates = len(country_data.dates)
#         if (len(country_data.total_cases) == 0):
#             country_data.total_cases = [0]*len_dates
#         if (len(country_data.daily_new_cases) == 0):
#             country_data.daily_new_cases = [0]*len_dates
#         if (len(country_data.active_cases) == 0):
#             country_data.active_cases = [0]*len_dates
#         if (len(country_data.daily_deaths) == 0):
#             country_data.daily_deaths = [0]*len_dates
#         if (len(country_data.new_recoveries) == 0):
#             country_data.new_recoveries = [0]*len_dates
#         new_list_of_all_country_data.append(country_data)
#     return new_list_of_all_country_data
