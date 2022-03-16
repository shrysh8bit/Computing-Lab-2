# from defer import return_value
# from numpy import _2Tuple
# from html_data import html_data
# from main_page import html_data
# from html_data import  html_data_full
# from ast import type_ignore
# from lib2to3.pgen2 import token

from itertools import count
import ply.lex as lex
import ply.yacc as yacc

import threading
import os

continent_counter = 0 # global variables which should be ideally absorbed within the function
world_counter = 0
country_counter = 0
data_hold_main = []

class DetailedOneDayData:
    entity_name = ''
    total_cases = 0
    active_cases = 0
    total_deaths = 0
    total_recovered = 0
    total_tests = 0
    deaths_per_million = 0
    tests_per_million = 0
    new_cases = 0
    new_deaths = 0
    new_recovered = 0


def getYesterdayData():
    # continents = ["Asia", "Europe", "North America", "South America", "Africa", "Australia/Oceania"]
    countries_list = [ "India", "Turkey", "Iran", "Indonesia", "Philippines", "Japan",
            "Israel", "Malaysia", "Thailand", "Viet-nam", "Iraq", "Bangladesh",
            "Pakistan", "Brazil", "Argentina", "Colombia", "Peru", "Chile",
            "Bolivia", "Uruguay", "Paraguay", "Venezuela", "South-Africa", "Morocco",
            "Tunisia", "Ethiopia", "Libya", "Egypt", "Kenya", "Zambia", "Algeria",
            "Botswana", "Nigeria", "Zimbabwe", "Australia", "Fiji", "Papua-New-Guinea",
            "New-Caledonia", "New-Zealand", "France", "UK", "Russia", "Italy", "Germany",
            "Spain", "Poland", "Netherlands", "Ukraine", "Belgium", "US", "Mexico", "Canada",
            "Cuba", "Costa-Rica", "Panama"]

    countries_dict = {} ## dict of country name to list[DateData]

    for item in countries_list:
        countries_dict[item] = []

    # data_hold_temp = [0]*12

    #Code to import html data, presently saved in external file to save time
    import requests
    url = 'https://www.worldometers.info/coronavirus/'
    html_data = requests.get(url)
    html_data = str(html_data.text)
    print("Please be patient, fetching and pre-proceesing the data may take appx 10 mins")
    print ("depending on the system")
    print ("Starting lex")

    # print(len(html_data_full))



    tokens = [ 'LTOTALCASES','CASES','SKIPTOKEN', 'LCONTINENT', 'RCONTINENT'
                , 'NAME', 'LWORLD', 'LCOUNTRY', 'ANCHOR']


    def t_LTOTALCASES(t):
        r'<td.+text-align.+>World'
        return t

    def t_SKIPTOKEN(t):
        r'</td>[\n\s\t]*<td>(\+)*'
        return t

    def t_CASES(t):
        # r'(\+){0,1}\d+(,\d+)*<|><'
        r'>\+*(\d)+(,\d+)*(.\d+)*.{0,1}<|><|(\+){0,1}\d+(,\d+)*<'
        return t

    def t_LCONTINENT(t):
        r'<.+data-continent=\".+\"'
        return t

    def t_RCONTINENT(t):
        r'\"\sstyle=\"display:\snone\">\n<.{2,4}><\/td>(\n<.+>){2}'
        return t

    def t_NAME(t):
        r'>[A-Za-z]+(\s|\/)*[A-Za-z/]+<'
        return t

    def t_LWORLD(t):
        r'total_row_body body_world'
        return t

    def t_LCOUNTRY(t):
        r'<td.+country.+\"'
        return t

    def t_ANCHOR(t):
        r'main_table_countries_yesterday\"'
        return t

    t_ignore = " \t\n"

    def t_error (t):
        t.lexer.skip(1)
        return

    lexer = lex.lex()
    lexer.input(html_data)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print ("tok : ", tok.type)



    ###################### End Of Lexer #########################################


    def p_start(t):
        '''start : world_cases
                | tcases
                | country_cases'''


    def p_world_cases(t):
        'world_cases : LTOTALCASES SKIPTOKEN CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES'
        global data_hold_temp
        global data_hold_main
        global world_counter
        world_counter += 1
        if world_counter != 2:
            pass
        else:
            # print("World cases : ", t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12])
            data_hold_temp = [0]*12
            data_hold_temp[1] = ">World<"
            data_hold_temp[2] = t[3]
            data_hold_temp[3] = t[9]
            data_hold_temp[4] = t[5]
            data_hold_temp[5] = t[7]
            data_hold_temp[6] = '0.001<'
            data_hold_temp[7] = t[12]
            data_hold_temp[8] = '0.001<'
            data_hold_temp[9] = t[4]
            data_hold_temp[10] = t[6]
            data_hold_temp[11] = t[8]
            # data_hold_temp[11] = t[10]
            data_hold_main.append(data_hold_temp)

    def p_tcases(t):
        '''tcases : LCONTINENT CASES NAME SKIPTOKEN CASES CASES CASES CASES CASES CASES CASES'''
        global data_hold_temp
        global data_hold_main
        global continent_counter
        continent_counter += 1
        if continent_counter < 7 or continent_counter > 12:
            pass
        else:
            # print("Cases :", t[3], t[5], t[6], t[7], t[8], t[9], t[10], t[11])
            data_hold_temp = [0]*12
            data_hold_temp[1] = t[3]
            data_hold_temp[2] = t[5]
            data_hold_temp[3] = t[11]
            data_hold_temp[4] = t[7]
            data_hold_temp[5] = t[9]
            data_hold_temp[6] = '0.001<'
            data_hold_temp[7] = '0.001<'
            data_hold_temp[8] = '0.001<'
            data_hold_temp[9] = t[6]
            data_hold_temp[10] = t[8]
            data_hold_temp[11] = t[10]
            data_hold_main.append(data_hold_temp)
            # data_hold_temp[9] = t[5]
            # data_hold_temp[10] = t[8]


    data_hold_temp = [0]*12

    def p_country_cases(t):
        'country_cases : LCOUNTRY NAME CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES CASES'
        global data_hold_temp
        global data_hold_main
        global country_counter
        country_counter += 1
        if country_counter < 200 or country_counter > 398:
            pass
        else:
            # print("Cases in county are :", t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15], t[16])
            data_hold_temp = [0]*12
            data_hold_temp[1] = t[2]
            data_hold_temp[2] = t[4]
            data_hold_temp[3] = t[9]
            data_hold_temp[4] = t[6]
            data_hold_temp[5] = t[7]
            data_hold_temp[6] = t[13]
            data_hold_temp[7] = t[12]
            data_hold_temp[8] = t[14]
            data_hold_temp[9] = t[5]
            data_hold_temp[10] = t[8]
            data_hold_main.append(data_hold_temp)



    def p_error(p):
        pass

    print("Lex Done")

    parser = yacc.yacc()
    parser.parse(html_data)
    print("Yacc Done")

    for item in data_hold_main:
        # remove angle brackets from country names
        item[1] = item[1].lstrip('>').rstrip('<')

    for item in data_hold_main:
        print(item)
    return data_hold_main


# input is a string after parsing. Remove angle brackets, and if only angle brackets,
# replace by zero
def stripAngleBrackets(input_string):
    if (type(input_string) is int):
        # parsed input can sometimes be integers
        return str(input_string)
    if (input_string == '><'):
        return '0'
    return input_string.lstrip('>').lstrip('+').rstrip('<')

# unformatted data is a list of lists
def formatData(unformatted_data):
    formatted_data = []
    for per_entity_list in unformatted_data:
        print('per entity data is ', per_entity_list)
        # print('THIS NEEDS TO BE FIXED!!')
        entity_data = DetailedOneDayData()
        entity_data.entity_name = per_entity_list[1]
        entity_data.total_cases = stripAngleBrackets(per_entity_list[2])
        entity_data.active_cases = stripAngleBrackets(per_entity_list[3])
        entity_data.total_deaths = stripAngleBrackets(per_entity_list[4])
        entity_data.total_recovered = stripAngleBrackets(per_entity_list[5])
        entity_data.total_tests = stripAngleBrackets(per_entity_list[6])
        entity_data.deaths_per_million = stripAngleBrackets(per_entity_list[7])
        entity_data.tests_per_million = stripAngleBrackets(per_entity_list[8])
        entity_data.new_cases = stripAngleBrackets(per_entity_list[9])
        entity_data.new_deaths = stripAngleBrackets(per_entity_list[10])
        entity_data.new_recovered = stripAngleBrackets(per_entity_list[11])
        formatted_data.append(entity_data)
    return formatted_data


yesterday_data_unformatted = getYesterdayData()
yesterday_data = formatData(yesterday_data_unformatted)
