# %%
'''
ETL Pipeline for scraping Player information from Ligainsider. Connected to Supabase 
'''

import bundesliga_standing
import ligainsider
import merger
import uuid
import config
import pandas as pd

import os
from supabase import create_client, Client
import json

# %%
# CONNECT TO SUPABASE DB
# Tutorial: https://www.analyticsvidhya.com/blog/2022/07/introduction-to-supabase-postgres-database-using-python/

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

'''
Suggested alternative; source: https://github.com/supabase-community/supabase-py
from supabase_client import Client
from dotenv import dotenv_values

config = dotenv_values(".env")

os.environ["SUPABASE_URL"] = config.SUPABASE_URL
os.environ["SUPABASE_KEY"] = config.SUPABASE_KEY


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
'''


# %%
supabase.table("kb_players_2021/22").select("*").execute()




# %%
data = {
    'timestamp': '2022-08-07 16:36:49',
    'Spieler': 'Joshua Kimmich',
    'team': 'Bayern Munich',
    'Position': 'Mittelfeldspieler',
    'Gesamtpunkte': 286,
    'Einsätze': 1,
    'Punkteschnitt': 286.0,
    'Marktwert': 54312593,
    'id': 'f5388ba2-c750-4cd7-9044-e1ae47102ea6'
}

supabase.table('kb_players_2022/23').insert(data).execute() # inserting one record
supabase
#supabase.table("kb_players_2022/23").select("*").execute()
#supabase.table("kb_players_2021/22").select("*").execute()

# %%
# SCRAPE CURRENT PLAYER DATA
bundesliga_standing = pd.DataFrame(bundesliga_standing.current_bundesliga_table()).iloc[: , :-1]
Ligainsider=pd.DataFrame(ligainsider.ligainsider_scraper())
Ligainsider_final = merger.merger(Ligainsider, bundesliga_standing)


# ADD UUID
Ligainsider_final['id'] = ''

for i in range(len(Ligainsider_final)):    
    Ligainsider_final['id'][i] =uuid.uuid4() #append uuid as primary key to identify each row 


# ADD TIMESTAMP
Ligainsider_final.insert(0, 'timestamp', pd.to_datetime('now').replace(microsecond=0)) #insert timestamp


# REDUCE DATAFRAME COLUMNS
Ligainsider_final = Ligainsider_final[['timestamp','Spieler','team','Position','Gesamtpunkte','Einsätze','Punkteschnitt','Marktwert','id']]

# Print DF
#Ligainsider_final

# %%

# UPLOAD TO SUPABASE DATABASE
supabase.table('kb_players_2022/23').insert(Ligainsider_final.to_json(default_handler=str)).execute() #convert pd df to json and upload to supabase


