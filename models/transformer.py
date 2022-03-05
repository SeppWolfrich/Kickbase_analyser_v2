import pandas as pd
import numpy as np

def transformer(x,y):
    
    Ligainsider = x
    bundesliga_standing = y
    
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

    #Ligainsider_final = Ligainsider
    Ligainsider_final = pd.merge(Ligainsider, bundesliga_standing, left_on='Verein',right_on='team') 
    Ligainsider_final = Ligainsider_final.drop('Verein',1)


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
    return Ligainsider_final