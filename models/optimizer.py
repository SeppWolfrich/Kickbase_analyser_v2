#%%
from pulp import *

from kickbase_api.kickbase import Kickbase
import pandas as pd
import numpy as np



    # Setup
pd.options.display.float_format = '{:,}'.format #generic format
pd.set_option("display.max_rows", None, "display.max_columns", None)


    # Import Kickbase Transfermarket Data

    # Connect api access point
kickbase = Kickbase()
    #username = input('Username: ')#"stephan.schulz@live.com"
    #password = getpass('Password: ')#"runescape"
    #kickbase.login(username, password)
kickbase.login("stephan.schulz@live.com", "runescape")
buli = kickbase.leagues()[1] #select active league
transfermarkt = kickbase.market(buli).players
#aktuellesTeam = kickbase.team_players(buli)

budget_available = kickbase.league_me(buli).budget
teamValue = kickbase.league_me(buli).team_value
#%%
kb_transfermarkt = []
for player in transfermarkt:
    kb_transfermarkt.append((player.first_name,  
                            player.last_name, 
                            player.average_points,
                            player.totalPoints, 
                            player.market_value,
                            player.market_value_trend,
                            player.position,
                            player.status,
                            player.team_id))
        
kb_transfermarkt_df = pd.DataFrame(kb_transfermarkt) #convert list to pd df
kb_transfermarkt_df.columns = ['first_name',
                            'last_name',
                            'average_points', 
                            'total_points', 
                            'market_value',
                            'market_value_trend',
                            'position',
                            'status',
                            'team'] #name columns


# Compute games played
kb_transfermarkt_df['games_played'] = (kb_transfermarkt_df['total_points'] / kb_transfermarkt_df['average_points']).round(1)
kb_transfermarkt_df['games_played'] = kb_transfermarkt_df['games_played'].fillna(0)


# Compute price per point column
kb_transfermarkt_df['price_per_point'] = kb_transfermarkt_df['market_value'] / kb_transfermarkt_df['average_points']
kb_transfermarkt_df['price_per_point'] = kb_transfermarkt_df['price_per_point'].round(2)


# Impute and replace values
kb_transfermarkt_df.loc[kb_transfermarkt_df.market_value_trend == 2, 'market_value_trend'] = 'down'
kb_transfermarkt_df.loc[kb_transfermarkt_df.market_value_trend == 1, 'market_value_trend'] = 'up'
kb_transfermarkt_df.loc[kb_transfermarkt_df.market_value_trend == 0, 'market_value_trend'] = 'same'

kb_transfermarkt_df.loc[kb_transfermarkt_df.price_per_point == np.inf, 'price_per_point'] = 0

kb_transfermarkt_df.loc[kb_transfermarkt_df.position == 1, 'position'] = 'GK'
kb_transfermarkt_df.loc[kb_transfermarkt_df.position == 2, 'position'] = 'DEF'
kb_transfermarkt_df.loc[kb_transfermarkt_df.position == 3, 'position'] = 'MF'
kb_transfermarkt_df.loc[kb_transfermarkt_df.position == 4, 'position'] = 'FWD'

kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 0, 'status'] = 'Fit'
kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 1, 'status'] = 'Injured'
kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 2, 'status'] = 'Bruised'
kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 4, 'status'] = 'Rehabd'
kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 8, 'status'] = 'Red Card'
kb_transfermarkt_df.loc[kb_transfermarkt_df.status == 16, 'status'] = 'Yellow Red Card'


# Map TeamID to Team name 
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '2', 'team'] = 'Bayern Munich'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '3', 'team'] = 'Dortmund'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '4', 'team'] = 'Eint Frankfurt'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '5', 'team'] = 'Freiburg'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '7', 'team'] = 'Leverkusen'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '9', 'team'] = 'Stuttgart'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '11', 'team'] = 'Wolfsburg'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '13', 'team'] = 'Augsburg'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '14', 'team'] = 'Hoffenheim'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '18', 'team'] = 'Mainz 05'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '19', 'team'] = 'Greuther Fürth'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '20', 'team'] = 'Hertha BSC'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '22', 'team'] = 'Arminia'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '24', 'team'] = 'Bochum'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '28', 'team'] = 'Köln'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '40', 'team'] = 'Union Berlin'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '43', 'team'] = 'RB Leipzig'
kb_transfermarkt_df.loc[kb_transfermarkt_df.team == '15', 'team'] = "M'Gladbach"


    # Output table
    #kb_transfermarkt_df.loc[kb_transfermarkt_df.price_per_point > 0].sort_values('price_per_point', ascending=True)
players_data = kb_transfermarkt_df.rename(columns={"market_value": "Marktwert", "position": "Positon", "total_points": "Gesamtpunkte"})
players_data['Name'] = players_data['first_name'].astype(str) +" "+ players_data["last_name"].astype(str)
players_data
#%%


players_data = players_data.loc[players_data['Marktwert'] > 1000000] # nur spieler mit marketwert über 1 * 10^6
#players_data["Punkte"] = players_data["Punkte"].replace([np.inf, np.nan, None], 0) # Spieler ohne punkte kriegen 0
players_data["Gesamtpunkte"] = players_data["Gesamtpunkte"].replace([np.inf, np.nan, None], 0)

players = list(players_data['Name'])
marktwert = dict(zip(players, players_data['Marktwert']))
position = dict(zip(players, players_data['Positon']))
punkte = dict(zip(players, players_data['Gesamtpunkte']))

player_vars = LpVariable.dicts("Player", players, lowBound=0, upBound=1, cat='Integer')

total_score = LpProblem("Kickbase_Team_Optimiert", LpMaximize)

total_score += lpSum([punkte[i] * player_vars[i] for i in players])
total_score += lpSum([marktwert[i] * player_vars[i] for i in players]) <= budget_available

vt = [p for p in players if position[p] == 'DEF'] #DEF -  Abwehrspieler
mt = [p for p in players if position[p] == 'MF'] # MF - Mittelfeldspieler
st = [p for p in players if position[p] == 'FWD'] #FWD - Stürmer

total_score += lpSum([player_vars[i] for i in vt]) == 5
total_score += lpSum([player_vars[i] for i in mt]) == 4
total_score += lpSum([player_vars[i] for i in st]) == 1

total_score.solve()

selected_players = [p for p in players if player_vars[p].varValue > 0]

# Create a DataFrame with selected players' information
selected_team_data = players_data[players_data['Name'].isin(selected_players)]
selected_team_data = selected_team_data[['Name', 'Marktwert', 'Positon', 'Gesamtpunkte']]

# Display the selected team as a DataFrame
print(selected_team_data)

# %%
for i in kickbase.line_up(buli).players:
    kickbase.player(i)
# %%
#kickbase.user.id

kickbase.league_feed(1, buli)
# %%
