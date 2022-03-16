from historicalData import *
# import historicalData as HD
from yesterdayData import *
# import yesterdayData as YD
import os
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
# countries_list = [ "India"]
continents_list = ["Asia", "Europe", "Africa", "North America", "South America", "Oceania"]

yesterday_data_unformatted = getYesterdayData()
# yesterday_data_unformatted = YD.yesterday_data_unformatted
yesterday_data = formatData(yesterday_data_unformatted)

list_of_all_country_data = parseHistoricalDataForGivenCountries(countries_list)
# list_of_all_country_data = HD.list_of_country_data

# main function which starts the user facing menu
def menuInit():
    os.system('clear')
    print('Welcome to the Coronavirus Worldometer Interactive Data Query System.')
    print('You can query yesterday\'s stats for the world, continents, or countries.')
    print('To view the possible inputs, please enter help')
    print('Else, please enter the name of the entity you wish to see the results for')
    text_input = input()
    # if(text_input == 'USA'):
    #     text_input = 'US'
    if (text_input == 'help'):
        return printHelpScreen()
    elif (text_input == 'World'):
        return printYesterdayData(text_input, False)
    elif (text_input in continents_list):
        return printYesterdayData(text_input, False)
    elif (text_input in countries_list):
        printYesterdayData(text_input, True)
        return dateRangeQuestionEntryPoint(text_input)
        # do countries stuff
    elif (text_input == 'exit'):
        return
    else:
        print("Your input didn't match any of the available options.")
        print("Press enter to reset the program. Remember that you can type help to view list of available commands")
        input()
        return menuInit()


def printYesterdayData(text_input, continue_follow_up_for_countries):
    entity_data = None
    for instance_of_entity_data in yesterday_data:
        if (instance_of_entity_data.entity_name == text_input):
            entity_data = instance_of_entity_data
            break
    if (entity_data == None):
        print('The data for the chosen country is presently not available, please try another country')
        input()
        return menuInit()
    print("Yesterday's data for "+entity_data.entity_name+" is as follows:")
    print("- total cases: "+entity_data.total_cases)
    print("- active cases: "+entity_data.active_cases)
    print("- total deaths: "+entity_data.total_deaths)
    print("- total recovered: "+entity_data.total_recovered)
    print("- total tests: "+entity_data.total_tests)
    print("- death/million: "+entity_data.deaths_per_million)
    print("- tests/million: "+entity_data.tests_per_million)
    print("- new case: "+entity_data.new_cases)
    print("- new death: "+entity_data.new_deaths)
    print("- new recovered: "+entity_data.new_recovered)
    if (continue_follow_up_for_countries):
        return

    print("This is all the data and functionality available for the given input.")
    print("Please press enter to get back to the previous screen.")
    input()
    return menuInit()

def printHelpScreen():
    print('\n')
    print("Please enter 'world' to see data from yesterday aggregated across all countries.")
    print("Please enter the name of any of the following continents to get data for them. The names are:")
    [print(continent_name+"  ") for continent_name in continents_list]
    print("Please enter the name of any of the following countries to get data for them. The names are:")
    [print(country_name+"  ") for country_name in countries_list]
    print("Please type exit to terminate the program.")
    print("Thank you for using, and I hope the above inputs were helpful. Press enter to go back to the previous screen.")
    input()
    return menuInit()


# We will only call this after yesterday's data has been shown for a country
# Hence when calling this function, we should always have the
def dateRangeQuestionEntryPoint(country):
    print('\n')
    print('In this section you can request statistics for '+country+' over a date range')
    print('Please input date in the format of Mmm DD, YYYY. For example, Feb 12, 2022 or Jan 03, 2021')
    print('Any other format of the date shall not be accepted.')
    print('If you wish to go back to the main screen, please enter back in the next prompt')
    print('Please enter the start date: ')
    start_date = input()
    print('Please enter the end date: ')
    end_date = input()

    if (start_date == 'back' or end_date == 'back'):
        return menuInit()

    # sanityCheck(list_of_all_country_data)
    # print('sanity check finished')
    country_data = None
    for instance_of_country_data in list_of_all_country_data:
        if (instance_of_country_data.country_name == country):
            country_data = instance_of_country_data
            break

    if(country_data == None):
        # print invalid inputs. Got to start of program
        print('Data not available for country. Restarting program.')
        return menuInit()

    perc_change_in_data = getPercChangeOverDateRange(country_data, start_date, end_date)
    if (perc_change_in_data == None):
        print('No data available for these dates. Please ensure you have mentioned correct dates in a valid format')
        return dateRangeQuestionEntryPoint(country)

    print('Perc change in data for active cases is '+"{:.2f}".format(perc_change_in_data.active_cases)+"%")
    print('Perc change in data for daily deaths is '+"{:.2f}".format(perc_change_in_data.daily_deaths)+"%")
    print('Perc change in data for new recovered is '+"{:.2f}".format(perc_change_in_data.new_recovered)+"%")
    print('Perc change in data for new cases is '+"{:.2f}".format(perc_change_in_data.new_cases)+"%")
    print('')
    closest_countries = getClosestCountries(perc_change_in_data, list_of_all_country_data, start_date, end_date)
    print('Closest country from perc active cases is '+closest_countries.active_cases_country_name+" with active cases change of "+"{:.2f}".format(closest_countries.active_cases_perc)+"%")
    print('Closest country from perc daily deaths is '+closest_countries.daily_deaths_country_name+" with daily deaths change of "+"{:.2f}".format(closest_countries.daily_deaths_perc)+"%")
    print('Closest country from perc new recovered is '+closest_countries.new_recovered_country_name+" with new recovered change of "+"{:.2f}".format(closest_countries.new_recovered_perc)+"%")
    print('Closest country from perc new cases is '+closest_countries.new_cases_country_name+" with new cases change of "+"{:.2f}".format(closest_countries.new_cases_perc)+"%")
    return showExitOrRestartScreen(country)


def showExitOrRestartScreen(country):
    print('\n')
    print("If you'd like to view data changes over more date ranges, please enter back at the next prompt")
    print("If you'd like to exit the program, please enter exit at the next prompt.")
    print("Else, please press any other key and press enter. Waiting for your input")
    text_input = input()
    if (text_input == 'back'):
        return dateRangeQuestionEntryPoint(country)
    elif (text_input == 'exit'):
        return
    else:
        return menuInit()

menuInit()
