'''
For testing & debugging
source ./venv/bin/activate

Bug Report 01.11.2022: Ligainsider removed a table which was scrapped. I had to switch the link and now the DF columns are fucked. 
I need to rename the columns but its not working for now. This is the code Ligainsider.rename(columns = {' Punkte ':'Gesamtpunkte', ' Ø–Punkte ':'Punkteschnitt', ' Marktwert ': 'Marktwert',' Einsätze ': 'Einsätze'}, inplace = True)
Also, no goali information available.
'''
# %%
import pandas as pd
from models import ligainsider

from models import bundesliga_standing
from models import ligainsider
from models import merger


# %%
bundesliga_standing = pd.DataFrame(bundesliga_standing.current_bundesliga_table()).iloc[: , :-1]
Ligainsider=pd.DataFrame(ligainsider.ligainsider_scraper())

# %%
df = merger.merger(Ligainsider, bundesliga_standing)
#%%
Ligainsider.rename(columns = {' Punkte Gesamt':'Gesamtpunkte', ' Ø–Punkte ':'Punkteschnitt', ' Marktwert ': 'Marktwert',' Einsätze ': 'Einsätze'}, inplace = True)
# %%
Ligainsider.columns
# %%


## Standard Libraries-----------------------------------------------
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

## Bundesliga Libraries---------------------------------------------
from soccer_data_api import SoccerDataAPI # Bundesliga standings
import requests # Scrape Bundesliga fixtures
import lxml.html as lh # Scrape Bundesliga fixtures


## SCRAPE DATA
# Get bundesliga standing from API
bundesliga_standing = pd.DataFrame(SoccerDataAPI().bundesliga()).iloc[: , :-1]  #current bundesliga table
bundesliga_standing
#%%
#Scaping Ligainsider page
ligainsider = 'https://www.ligainsider.de/stats/kickbase/rangliste/feldspieler/durchschnitt/' #I had to change the link which removed Keeper Scores and messed up the DF structure (check 69)
page_player_information = requests.get(ligainsider) #Create a handle, page, to handle the contents of the website

doc = lh.fromstring(page_player_information.content) #Store the contents of the website under doc

tr_elements = doc.xpath('//tr') #Parse data that are stored between <tr>..</tr> of HTML


#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))


#Since our first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 8, the //tr data is not from our table 
    if len(T)!=9:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1



Dict={title:column for (title,column) in col}
Ligainsider=pd.DataFrame(Dict)
Ligainsider
#%%
Ligainsider.rename(columns = {' Punkte ':'Gesamtpunkte', ' Ø–Punkte ':'Punkteschnitt', ' Marktwert ': 'Marktwert',' Einsätze ': 'Einsätze'}, inplace = True) #Had to rename columns. This is still casuing issues in the local model

Ligainsider = Ligainsider[['Spieler','Verein','Position','Gesamtpunkte','Einsätze','Punkteschnitt','Marktwert']]


Ligainsider.loc[Ligainsider.Verein == 'FC Bayern München', 'Verein'] = 'Bayern Munich'#
Ligainsider.loc[Ligainsider.Verein == 'Borussia Dortmund', 'Verein'] = 'Dortmund'#
Ligainsider.loc[Ligainsider.Verein == 'Eintracht Frankfurt', 'Verein'] = 'Eint Frankfurt'#
Ligainsider.loc[Ligainsider.Verein == 'SC Freiburg', 'Verein'] = 'Freiburg'#
Ligainsider.loc[Ligainsider.Verein == 'Bayer 04 Leverkusen', 'Verein'] = 'Leverkusen'#
Ligainsider.loc[Ligainsider.Verein == 'VfB Stuttgart', 'Verein'] = 'Stuttgart'#
Ligainsider.loc[Ligainsider.Verein == 'VfL Wolfsburg', 'Verein'] = 'Wolfsburg'#
Ligainsider.loc[Ligainsider.Verein == 'FC Augsburg', 'Verein'] = 'Augsburg'#
Ligainsider.loc[Ligainsider.Verein == 'TSG 1899 Hoffenheim', 'Verein'] = 'Hoffenheim'#
Ligainsider.loc[Ligainsider.Verein == '1. FSV Mainz 05', 'Verein'] = 'Mainz 05'#
Ligainsider.loc[Ligainsider.Verein == 'SpVgg Greuther Fürth', 'Verein'] = 'Greuther Fürth'#
Ligainsider.loc[Ligainsider.Verein == 'Hertha BSC', 'Verein'] = 'Hertha BSC'#
Ligainsider.loc[Ligainsider.Verein == 'Arminia Bielefeld', 'Verein'] = 'Arminia'#
Ligainsider.loc[Ligainsider.Verein == 'VfL Bochum', 'Verein'] = 'Bochum'#
Ligainsider.loc[Ligainsider.Verein == '1. FC Köln', 'Verein'] = 'Köln'#
Ligainsider.loc[Ligainsider.Verein == '1. FC Union Berlin', 'Verein'] = 'Union Berlin'#
Ligainsider.loc[Ligainsider.Verein == 'RB Leipzig', 'Verein'] = 'RB Leipzig'#
Ligainsider.loc[Ligainsider.Verein == 'Borussia Mönchengladbach', 'Verein'] = "M'Gladbach" #
Ligainsider.loc[Ligainsider.Verein == 'Darmstadt 98', 'Verein'] = "Darmstadt 98" #
Ligainsider.loc[Ligainsider.Verein == '1. FC Heidenheim', 'Verein'] = "Heidenheim" #
Ligainsider.loc[Ligainsider.Verein == 'SV Werder Bremen', 'Verein'] = "Werder Bremen" #
Ligainsider
#%%
#Ligainsider_final = Ligainsider
Ligainsider_final = pd.merge(Ligainsider, bundesliga_standing, left_on='Verein',right_on='team') 
Ligainsider_final
#%%
Ligainsider_final.drop('Verein', axis=1, inplace=True)
Ligainsider_final
#%%

# Cleaning and converting
Ligainsider_final['Spieler'] = [x.replace('\n', '') for x in Ligainsider_final['Spieler']] #removes /n 
Ligainsider_final['Spieler'] = Ligainsider_final['Spieler'].astype(str)

Ligainsider_final['Gesamtpunkte'] = [x.replace('.', '') for x in Ligainsider_final['Gesamtpunkte'].astype(str)] #remove commas or dots
Ligainsider_final['Gesamtpunkte'] = Ligainsider_final['Gesamtpunkte'].astype(int)

Ligainsider_final['Einsätze'] = Ligainsider_final['Einsätze'].replace('', 0)  #replace blanks with 0
Ligainsider_final['Einsätze'] = Ligainsider_final['Einsätze'].astype(int)

Ligainsider_final['Punkteschnitt'] = Ligainsider_final['Gesamtpunkte']/Ligainsider_final['Einsätze']
Ligainsider_final['Punkteschnitt'] = Ligainsider_final['Punkteschnitt'].fillna(0)
Ligainsider_final['Punkteschnitt'] = Ligainsider_final['Punkteschnitt'].round(2)

Ligainsider_final['Marktwert'] = [x.replace('.', '') for x in Ligainsider_final['Marktwert']] #remove commas or dots
Ligainsider_final['Marktwert'] = Ligainsider_final['Marktwert'].str.replace('€', '') #remove € sign
Ligainsider_final['Marktwert'] = Ligainsider_final['Marktwert'].astype(int)

Ligainsider_final['PreisProPunkt'] = (Ligainsider_final['Marktwert']/Ligainsider_final['Gesamtpunkte']).round(2) #compute price per point
Ligainsider_final.loc[Ligainsider_final.PreisProPunkt == np.inf, 'PreisProPunkt'] = 0
#Ligainsider_final.dtypes #check data types of columns
#Ligainsider_final['Spieler']
df = Ligainsider_final
# %%
