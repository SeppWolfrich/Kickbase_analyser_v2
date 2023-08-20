from soccer_data_api import SoccerDataAPI 

'''
This scrapes the Bundesliga table
'''

def current_bundesliga_table():
    return SoccerDataAPI().bundesliga()
