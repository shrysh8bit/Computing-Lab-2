# from html_data import  html_data
import requests
# from pprint import pprint

import ply.lex as lex
import ply.yacc as yacc
# main_data = []
# temp_data = []

class ConsolidatedDataPerCountry:
    country_name = ''
    dates = []
    total_cases = []
    daily_new_cases = []
    active_cases = []
    daily_deaths = []
    new_recoveries = []


class PercentageChangeInData:
    country_name = ''
    active_cases = 0
    daily_deaths = 0
    new_recovered = 0
    new_cases = 0


class DataPerDate:
    date = ''
    active_cases = 0
    daily_deaths = 0
    new_recovered = 0
    new_cases = 0

# 0 - dates
# 1 - total cases
# 2 - daily new cases
# 3 - active cases
# 4 - daily deaths
# 5 - new recoveries

countries_list = [ "India", "Turkey", "Iran", "Indonesia", "Philippines", "Japan",
            "Israel", "Malaysia", "Thailand", "Viet-nam", "Iraq", "Bangladesh",
            "Pakistan", "Brazil", "Argentina", "Colombia", "Peru", "Chile",
            "Bolivia", "Uruguay", "Paraguay", "Venezuela", "South-Africa", "Morocco",
            "Tunisia", "Ethiopia", "Libya", "Egypt", "Kenya", "Zambia", "Algeria",
            "Botswana", "Nigeria", "Zimbabwe", "Australia", "Fiji", "Papua-New-Guinea",
            "New-Caledonia", "New-Zealand", "France", "UK", "Russia", "Italy", "Germany",
            "Spain", "Poland", "Netherlands", "Ukraine", "Belgium", "US", "Mexico", "Canada",
            "Cuba", "Costa-Rica", "Panama"]

# countries_list = [ "India", "Turkey", "Iran", "Indonesia", "Philippines", "Japan"]
# countries_list = [ "Japan"]


countries_list.sort()
countries_dict = {} ## dict of country name to list[DateData]

# for country_name in countries_list:
#     countries_dict[country_name] = []
    # countries_dict[item] = [[0,-1],[0,-1],[0,-1],[0,-1],[0,-1],[0,-1]]

# Output is a list with data for all countries. Each element in a list contains
# information for one country


# def updateCountryNamesInYesterdayData(historical_data):
#     updated_names = {'Viet-nam':'Vietnam', 'US':'USA', 'Costa-Rica': 'Costa Rica', 
#                 'New-Caledonia':'New Caledonia', 'New-Zealand': 'New Zealand',
#                 'Papua-New-Guinea': 'Papua New Guinea', 'South-Africa': 'South Africa',}

#     for country_historical_data in historical_data:
#         if country_historical_data.country_name in updated_names:
#             country_historical_data.country_name = updated_names[country_historical_data.country_name]

#     return historical_data



def parseHistoricalDataForGivenCountries(countries_list):
    list_of_country_data = []
    for country_name in countries_list:
        print("Getting data for : ", country_name)
        url = "https://www.worldometers.info/coronavirus/country/" + country_name + "/"
        html_data = requests.get(url)
        html_data = str(html_data.content)
        print ("html data retrieved")

        country_data = ConsolidatedDataPerCountry()

        # if country_name == 'US':
        #     country_name = 'USA'

        country_data.country_name = country_name
        # countries_dict[country_name] = html_data

    # print("Getting data for India")
    # url = "https://www.worldometers.info/coronavirus/country/india/"
    # html_data = requests.get(url)
    # html_data = str(html_data.content)
    # countries_dict["India"] = html_data
    # print (len(html_data), type(html_data))
    # print ( type(html_data))




        tokens = [ 'TOTAL_CASES','LINEAR_SCALE', 'DATE_RANGE' , 'DATA',
                'DAILY_CASES', 'ACTIVE_CASES', 'DEATHS', 'BREAK', 'NEW_RECOVER']

        def t_TOTAL_CASES(t):
            r'Total\sCases'
            return t

        def t_LINEAR_SCALE(t):
            r'Linear\sScale'
            return t

        def t_DATE_RANGE(t):
            r'\[(,*\".{12}\")+\]'
            return t

        def t_DATA(t):
            r'\[(null,)*\d+(,\d+)+\]'
            return t

        def t_ACTIVE_CASES(t):
            r'>Active\sCases'
            return t

        def t_DAILY_CASES(t):
            r'\'Daily\sCases'
            return t

        def t_DEATHS(t):
            r'.Daily\sDeaths'
            return t

        def t_BREAK(t):
            r'<style>'
            return t

        def t_NEW_RECOVER(t):
            r'\'New\sRecoveries'
            return t


        t_ignore = " \t\n"

        def t_error (t):
            t.lexer.skip(1)
            return



        lexer = lex.lex()
        lexer.input(html_data)

        while True:
            tok = lexer.token()
            if not tok:
                break
            # print ("tok : ", tok.type)

        # print("Lex Done")


        ###################### End Of Lexer #########################################


        def p_start(t):
            '''start : total_cases
                    | daily
                    | active
                    | dead_ppl
                    | new_recover'''



        def p_total_cases(t):
            'total_cases : TOTAL_CASES LINEAR_SCALE DATE_RANGE DATA'
            # global main_data
            # global countries_dict
            dates = t[3]
            new = dates[2:-2]
            new = new.replace('","', ';')
            new = new.split(";")
            # main_data.append(new)
            country_data.dates = new

            cases = t[4]
            new = cases[1:-1]
            new = new.split(",")
            new = [0 if x=='null' else x for x in new]
            # main_data.append(new)
            country_data.total_cases = new
            # print ("The dates for total cases are : ", t[1])


        def p_daily(t):
            'daily : DAILY_CASES DATA'
            # global main_data
            cases = t[2]
            new = cases[1:-1]
            new = new.split(",")
            new = [0 if x=='null' else x for x in new]
            # main_data.append(new)
            country_data.daily_new_cases = new
            # print("In daily new cases", t[1])

        def p_active(t):
            'active : DEATHS ACTIVE_CASES DATE_RANGE DATA'
            # global main_data
            cases = t[4]
            new = cases[1:-1]
            new = new.split(",")
            new = [0 if x=='null' else x for x in new]
            # main_data.append(new)
            country_data.active_cases = new
            # print ("In active cases")

        def p_dead_ppl(t):
            'dead_ppl : DEATHS DATA DATA DATA'
            # global main_data
            cases = t[2]
            new = cases[1:-1]
            new = new.split(",")
            new = [0 if x=='null' else x for x in new]
            # main_data.append(new)
            country_data.daily_deaths = new
            # print("In daily deaths")

        def p_new_recover(t):
            'new_recover : NEW_RECOVER DATA'
            # global main_data
            cases = t[2]
            new = cases[1:-1]
            new = new.split(",")
            new = [0 if x=='null' else x for x in new]
            # main_data.append(new)
            country_data.new_recoveries = new
            # print("In new Recoveries")

        def p_error(p):
            pass




        parser = yacc.yacc()
        parser.parse(html_data)
        # print("Yacc Done")

        list_of_country_data.append(country_data)
        # print(country_data.country_name)
        list_of_country_data = replaceEmptyListByZeroArray(list_of_country_data)

        print ("End Of Parsing for : ", country_name)
        

        updated_names = {'Viet-nam':'Vietnam', 'US':'USA', 'Costa-Rica': 'Costa Rica', 
                'New-Caledonia':'New Caledonia', 'New-Zealand': 'New Zealand',
                'Papua-New-Guinea': 'Papua New Guinea', 'South-Africa': 'South Africa',}

        # for country_historical_data in historical_data:
        if country_data.country_name in updated_names:
            country_data.country_name = updated_names[country_data.country_name]
            print ("New country name is :", country_data.country_name )

        print("\n")




        # list_of_all_country_data = updateCountryNamesInYesterdayData(list_of_all_country_data)

    return list_of_country_data


# Fills PercentageChangeInData for a given country over the date range
def getPercChangeOverDateRange(country_data, start_date, end_date):
    start_date_data = extractDataForDate(country_data, start_date)
    end_date_data = extractDataForDate(country_data, end_date)
    if (start_date_data == None or end_date_data == None):
        return None
    return calcPercChangeInData(start_date_data, end_date_data, country_data.country_name)


# For two given sets of data, calculate percentage change
def calcPercChangeInData(start_data, end_data, country_name):
    start_data = handleZeroesInData(start_data)
    perc_change_in_data = PercentageChangeInData()
    perc_change_in_data.country_name = country_name
    perc_change_in_data.active_cases = (end_data.active_cases - start_data.active_cases)*100.0/start_data.active_cases
    perc_change_in_data.daily_deaths = (end_data.daily_deaths - start_data.daily_deaths)*100.0/start_data.daily_deaths
    perc_change_in_data.new_recovered = (end_data.new_recovered - start_data.new_recovered)*100.0/start_data.new_recovered
    perc_change_in_data.new_cases = (end_data.new_cases - start_data.new_cases)*100.0/start_data.new_cases
    return perc_change_in_data


# replace 0 by 0.0001 to not break the percentage calculation
def handleZeroesInData(data_for_date):
    replacement_for_zero = 0.0001
    if (data_for_date.active_cases == 0):
        data_for_date.active_cases = replacement_for_zero
    if (data_for_date.daily_deaths == 0):
        data_for_date.daily_deaths = replacement_for_zero
    if (data_for_date.new_recovered == 0):
        data_for_date.new_recovered = replacement_for_zero
    if (data_for_date.new_cases == 0):
        data_for_date.new_cases = replacement_for_zero
    return data_for_date


# Return None if data not found for Date. Else extract all date for that date
def extractDataForDate(country_data, date):
    for index in range(0, len(country_data.dates)):
        if (country_data.dates[index] == date):
            data_for_date = DataPerDate()
            data_for_date.date = date
            data_for_date.active_cases = int(country_data.active_cases[index])
            data_for_date.daily_deaths = int(country_data.daily_deaths[index])
            data_for_date.new_recovered = int(country_data.new_recoveries[index])
            data_for_date.new_cases = int(country_data.daily_new_cases[index])
            return data_for_date
    return None


class ClosestCountries:
    active_cases_country_name = 'dummy'
    active_cases_perc = 99999999
    daily_deaths_country_name = 'dummy'
    daily_deaths_perc = 99999999
    new_recovered_country_name = 'dummy'
    new_recovered_perc = 99999999
    new_cases_country_name = 'dummy'
    new_cases_perc = 99999999


def getClosestCountries(target_perc_change_in_data, list_of_all_country_data, start_date, end_date):
    closest_countries = ClosestCountries()
    for instance_of_country_data in list_of_all_country_data:
        if (instance_of_country_data.country_name == target_perc_change_in_data.country_name):
            continue
        perc_change_in_data = getPercChangeOverDateRange(instance_of_country_data, start_date, end_date)
        if (abs(closest_countries.active_cases_perc) > abs(target_perc_change_in_data.active_cases - perc_change_in_data.active_cases)):
            closest_countries.active_cases_country_name = instance_of_country_data.country_name
            closest_countries.active_cases_perc = perc_change_in_data.active_cases
        if (abs(closest_countries.daily_deaths_perc) > abs(target_perc_change_in_data.daily_deaths - perc_change_in_data.daily_deaths)):
            closest_countries.daily_deaths_country_name = instance_of_country_data.country_name
            closest_countries.daily_deaths_perc = perc_change_in_data.daily_deaths
        if (abs(closest_countries.new_recovered_perc) > abs(target_perc_change_in_data.new_recovered - perc_change_in_data.new_recovered)):
            closest_countries.new_recovered_country_name = instance_of_country_data.country_name
            closest_countries.new_recovered_perc = perc_change_in_data.new_recovered
        if (abs(closest_countries.new_cases_perc) > abs(target_perc_change_in_data.new_cases - perc_change_in_data.new_cases)):
            closest_countries.new_cases_country_name = instance_of_country_data.country_name
            closest_countries.new_cases_perc = perc_change_in_data.new_cases
    return closest_countries


def sanityCheck(list_of_all_country_data):
    for country_data in list_of_all_country_data:
        print('country name is ', country_data.country_name)
        print('len dates is ', len(country_data.dates), '  ', len(country_data.total_cases), ' ', len(country_data.daily_new_cases), '  ', len(country_data.active_cases), '  ', len(country_data.daily_deaths), '  ', len(country_data.new_recoveries))


# When building country data, we get empty list if data is not present
# This replaces that empty list by an array of zeroes
def replaceEmptyListByZeroArray(list_of_all_country_data):
    new_list_of_all_country_data = []
    for country_data in list_of_all_country_data:
        len_dates = len(country_data.dates)
        if (len(country_data.total_cases) == 0):
            country_data.total_cases = [0]*len_dates
        if (len(country_data.daily_new_cases) == 0):
            country_data.daily_new_cases = [0]*len_dates
        if (len(country_data.active_cases) == 0):
            country_data.active_cases = [0]*len_dates
        if (len(country_data.daily_deaths) == 0):
            country_data.daily_deaths = [0]*len_dates
        if (len(country_data.new_recoveries) == 0):
            country_data.new_recoveries = [0]*len_dates
        new_list_of_all_country_data.append(country_data)
    return new_list_of_all_country_data

list_of_all_country_data = parseHistoricalDataForGivenCountries(countries_list)




# for entry in list_of_all_country_data:
#     print(entry.country_name)


# # list_of_all_country_data = updateCountryNamesInYesterdayData(list_of_all_country_data)

# for entry in list_of_all_country_data:
#     print(entry.country_name)