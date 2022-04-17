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

date_news_2019 = []

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

def dateFormatting(date_in_str):
    date_in_str = date_in_str.lstrip('>')
    date_in_str = date_in_str.rstrip('<')
    mm_yyyy = date_in_str.split()
    # print(mm_yyyy)
    dd = int(mm_yyyy[0])
    # mm = 12
    date_list = [0]*3
    date_list[0] = dd
    date_list[1] = 12
    date_list[2] = 2019

    return date_list
    # print(date_list)


# str_date = '>1 December<'
# suffix = 'December 2019'
# dateFormatting(str_date)

def parseWorldWideNews():
    url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_2019'
    html_data_raw = requests.get(url)
    html_data_str = (html_data_raw.text)
    html_data_str = splitInputStr(html_data_str, 350, 430)


    print ("December 2019", len(html_data_str))

    tokens = [ 'DATE', 'DATE_ANCHOR', 'NEWS', 'BREAK']
    
    def t_BREAK(t):
        r'<h2>'
        return t

    def t_DATE_ANCHOR(t):
        r'<span class=\"mw-headline\"'
        return t

    def t_DATE(t):
        r'>\d{1,2}\s{1}\w{3,12}<'
        return t

    def t_NEWS(t):
        r'<p>.+'
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


    ########################## End Of Lexer #########################################

    def p_start(t):
        '''start : news1'''
                

    def p_news1(t):
        'news1 : DATE NEWS'
        # print ("DATES1 : ", t[1], t[2]) 
        news_instance = newsItems()
        str_date = t[1]
        int_date_list = dateFormatting(str_date)
        news_instance.day = int_date_list[0]
        news_instance.month = int_date_list[1]
        news_instance.year = int_date_list[2]
        news_instance.news = cleanReadData(t[2])
        news_instance.country = 'World'
        global date_news_2019
        date_news_2019.append(news_instance)

    def p_error(p):
        pass
    
    parser = yacc.yacc()
    parser.parse(html_data_str)
    # print("Yacc Done")


parseWorldWideNews()    

# for item in date_news_2019:
#     print (item.day, item.month, item.year, item.news)