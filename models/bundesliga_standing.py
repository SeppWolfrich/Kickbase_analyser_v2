from soccer_data_api import SoccerDataAPI 

def current_bundesliga_table():
    return SoccerDataAPI().bundesliga()
