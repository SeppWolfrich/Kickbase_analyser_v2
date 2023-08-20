'''
This is the main Streamlit app

https://www.youtube.com/watch?v=W--_EOzdTHk tutotial
activate venv: source venv/bin/activate
python3 -m pip install "package name" installing packages
python3 -m streamlit run /Users/stephanschulz/Documents/Coding/Python/MiniProjects/Kickbase/kickbase_analyser/main.py
'''


# Load Libraries
from models import bundesliga_standing
from models import ligainsider
from models import merger

import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components #to embed twitter profile
import altair as alt
import matplotlib.pyplot as plt

# Main code
if __name__ == '__main__':
    
    # Setup Raw Data
    bundesliga_standing = pd.DataFrame(bundesliga_standing.current_bundesliga_table()).iloc[: , :-1]
    Ligainsider=pd.DataFrame(ligainsider.ligainsider_scraper())
    df = merger.merger(Ligainsider, bundesliga_standing)

    # Visualise
    st.set_page_config(layout="wide") # page expands to full width
    st.title("Kickbase Analyser v1.0 (WIP)")

    # Twitter & Mail Link
    #st.caption('By [Sepp Wolfrich](https://twitter.com/SeppWolfrich). Feedback gerne direkt an mich via Twitter!')
    st.markdown('<p> Created by Sepp Wolfrich. Feedback gerne direkt an mich via <a href="https://twitter.com/SeppWolfrich">Twitter</a> oder <a href="mailto:joseppwolfrich@gmail.com?subject=Kickbase Analyser Feedback!">Mail!</a> </p>', unsafe_allow_html=True)

    # General analysis
    #st.header('Generelle Analyse aller Spieler der Bundesliga unabhängig vom Verein')
    st.subheader('Durchschnittliche Punkte (gesamte Bundesliga)')
    st.caption('Durchschnittliche Gesamtpunkte aller Spieler der Bundesliga mit mehr als 0 Einsätzen.')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Torhüter Punkte", round(df.loc[(df['Position'] == 'Torhüter') & (df['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col2.metric("Verteidiger Punkte", round(df.loc[(df['Position'] == 'Abwehrspieler') & (df['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col3.metric("Mittelfeld Punkte", round(df.loc[(df['Position'] == 'Mittelfeldspieler') & (df['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col4.metric("Stürmer Punkte", round(df.loc[(df['Position'] == 'Stürmer') & (df['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))



    # Per Team Deep Dive
    st.subheader('Team Analyse')

    selected_team = st.selectbox("Select Team", (df['team'].unique()))
    df1 = df[df['team']==selected_team]


    # Show table of team if clicked
    if st.checkbox("Show Rawdata"):
        st.write(df1[['Spieler','Marktwert','Gesamtpunkte','Punkteschnitt', 'PreisProPunkt', 'Einsätze']].sort_values('Gesamtpunkte', ascending = False))


    col1, col2, col3 = st.columns(3)
    col1.metric('Tabellenplatz', df1['pos'].iloc[0])

    Gesamtpunkte = df1['Gesamtpunkte'].astype(float).sum().round(2)
    Gesamtpunkte_adjusted = "{:,.0f}".format(Gesamtpunkte)
    col2.metric('Gesamtpunkte', Gesamtpunkte_adjusted)

    Marktwert = df1['Marktwert'].astype(float).sum().round(2)
    Marktwert_EUR = "€{:,.0f}".format(Marktwert)
    col3.metric('Gesamtmarktwert', Marktwert_EUR)


    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Torhüter Punkte", round(df1.loc[(df1['Position'] == 'Torhüter') & (df1['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col2.metric("Verteidiger Punkte", round(df1.loc[(df1['Position'] == 'Abwehrspieler') & (df1['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col3.metric("Mittelfeld Punkte", round(df1.loc[(df1['Position'] == 'Mittelfeldspieler') & (df1['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))
    col4.metric("Stürmer Punkte", round(df1.loc[(df1['Position'] == 'Stürmer') & (df1['Einsätze'] != 0), 'Gesamtpunkte'].mean(),2))


    # Per Team Visuals
    st.altair_chart(alt.Chart(df1).mark_bar().encode(
        x=alt.X('Spieler', sort='-y'),
        y='Gesamtpunkte', color = 'Position',
        tooltip=["Spieler","Gesamtpunkte",'PreisProPunkt',"Position"]
    ).interactive(),use_container_width=True)

    st.altair_chart(alt.Chart(df1).mark_bar().encode(
        x=alt.X('Spieler', sort='-y'),
        y='Punkteschnitt', color = 'Position',
        tooltip=["Spieler","Punkteschnitt",'PreisProPunkt',"Position"]
    ).interactive(),use_container_width=True)

    st.altair_chart(alt.Chart(df1).mark_bar().encode(
        x=alt.X('Spieler', sort='-y'),
        y='Marktwert', color = 'Position',
        tooltip=["Spieler","Gesamtpunkte",'Marktwert','PreisProPunkt',"Position"]
    ).interactive(),use_container_width=True)


    # Per Player Visuals
    st.subheader('Spieler Analyse')
    st.caption('Ausgewählter Spieler wird mit allen anderen Spielern der gleichen Position verglichen. Ausgewählter Spieler ist rot markeiert. Spieler unterhalb der orangenen Linie erzielen durschnittlich überproportional viele Punkte für ihren Marktwert.')

    #selected_player = st.multiselect("Select Player", (df['Spieler'].unique())) #single selection
    #df2 = df[df['Spieler']==[selected_player]] #select player based on selection in col1

    selected_player = st.multiselect("Select Player", 
                                    options = df['Spieler'].unique(), #df['Spieler'].unique()
                                    default = df['Spieler'][0]) #default = ['Robert Lewandowksi','Erling Haaland']
    st.caption('Für einen genauen Vergleich, bitte nur Spieler der gleichen Position auswählen. Wenn kein Spieler ausgewählt ist, resultiert das in einem Error.')

    #schools = st.multiselect("Team", teamsList, default = ['USC','Nebraska','Texas','Alabama', 'Ohio State'])

    df2 = df[df['Spieler'].isin(selected_player)] #filtering dataframe by list selected in selected_players
    df_base = df.loc[df['Position'] == df2.iloc[0][1]] #filter dataset based on position


    # Plotting Gesamtpunkte v Marktwert -----------
    chart = alt.Chart(df_base).mark_circle(size=60).encode( #chart for all players
        x='Gesamtpunkte',
        y='Marktwert',
        color=alt.value('grey'), #defaults all players to grey
        #size = 'Einsätze',
        tooltip=['Spieler', 'Gesamtpunkte','Punkteschnitt', 'Marktwert', 'Einsätze' ,'Position','team']
    )#.interactive()

    chart2 = alt.Chart(df2).mark_circle(size=60).encode( #chart for selected players
        x='Gesamtpunkte',
        y='Marktwert',
        #color=alt.value('red'),
        color='Spieler', #each player is assingned one color
        #size = 'Punkteschnitt',
        tooltip=['Spieler', 'Gesamtpunkte','Punkteschnitt', 'Marktwert', 'Einsätze' ,'Position','team']
    )#.interactive()

    st.altair_chart((chart + chart2 + chart.transform_regression('Gesamtpunkte', 'Marktwert').mark_line(color="orange")), use_container_width = True)


    # Plotting Punkteschnitt v Marktwert -----------
    chart3 = alt.Chart(df_base).mark_circle(size=60).encode( #chart for all players
        x='Punkteschnitt',
        y='Marktwert',
        color=alt.value('grey'), #defaults all players to grey
        #size = 'Punkteschnitt',
        tooltip=['Spieler', 'Gesamtpunkte','Punkteschnitt', 'Marktwert', 'Einsätze' ,'Position','team']
    )#.interactive()

    chart4 = alt.Chart(df2).mark_circle(size=60).encode( #chart for selected players
        x='Punkteschnitt',
        y='Marktwert',
        #color=alt.value('red'),
        color='Spieler', #each player is assingned one color
        #size = 'Punkteschnitt',
        tooltip=['Spieler', 'Gesamtpunkte','Punkteschnitt', 'Marktwert', 'Einsätze' ,'Position','team']
    )#.interactive()

    st.altair_chart((chart3 + chart4 + chart3.transform_regression('Punkteschnitt', 'Marktwert').mark_line(color="orange")), use_container_width = True)
    #+ chart.transform_regression('Gesamtpunkte', 'Marktwert', method="poly").mark_line()