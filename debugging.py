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
Ligainsider.rename(columns = {' Punkte ':'Gesamtpunkte', ' Ø–Punkte ':'Punkteschnitt', ' Marktwert ': 'Marktwert',' Einsätze ': 'Einsätze'}, inplace = True)
# %%
Ligainsider.columns
# %%
