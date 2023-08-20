'''
Statistical evaluation of model used to predict fair value of players. Conceptually the model takes to variables into 
consideration, performance and potential. 
Performance is based on the actual performance of a player and operationalised mainly using total points, points per game, 
games played and position.
Potential is operationalised using a historic and an actual component. The histroric component is the team the player plays 
for (e.g. historically, on average a Bayern Munich Player has more potential of scoring points than a Bochum player), 
which is represented by a club index score and the actual performance of the team which is represented by the points the team
has currently accumulated (could as well be represented by the rank as this takes into consideration more factors such as
goal diffference, etc.)
Both variables are then normalized/ standardized and computed with a regression to output a fair value price for the player.
'''
# %%
# Load Libraries
import bundesliga_standing
import ligainsider
import ligainsider_performanceindex
import merger

import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
import statsmodels.api as sm

# %%
# Setup df
bundesliga_standing = pd.DataFrame(bundesliga_standing.current_bundesliga_table()).iloc[: , :-1]
Ligainsider=pd.DataFrame(ligainsider.ligainsider_scraper())
df_merge = merger.merger(Ligainsider, bundesliga_standing)

performance_index = ligainsider_performanceindex.performance_index()

df = pd.merge(df_merge, performance_index, on='Spieler', how='left') 

df['Ø–Note Gesamt'] = df['Ø–Note Gesamt'].fillna(6)
df['Ø–Min. Gesamt'] = df['Ø–Min. Gesamt'].fillna(0)
# %%
# Investigating dataset 
df.head()
df.describe()
df.dtypes
# %%
df.head()

# %%
# convert object to int columns
df['points'] = df['points'].astype('int')
df['pos'] = df['pos'].astype('int')
# %%
plt.hist(np.sqrt(df['Gesamtpunkte']))
# %%
sns.pairplot(df) # Corrplot

# %%
plt.figure(figsize=(14,8))
sns.set_theme(style="white")
corr = df.corr()
heatmap = sns.heatmap(corr, annot=True, cmap="Blues", fmt='.1g')

# %%
# Z score transformation / standardisation
y = df['Marktwert']
X_stand = df[['Gesamtpunkte', 'pos', 'Einsätze']].dropna().apply(stats.zscore)
X_stand = sm.add_constant(X_stand)
model11 = sm.OLS(y, X_stand).fit()
model11.summary()

ypred = model11.predict(X_stand) 

plt.scatter(X_stand['pos'],y)
plt.plot(X_stand['pos'],ypred)


#8.977e+06 + 7.431e+06*4.454362 -1.34e+06*-1.664528
# %%
# Multiple Regression
y = df['Marktwert']
X = df[['Gesamtpunkte', 'pos', 'Einsätze']]
X = sm.add_constant(X)
model11 = sm.OLS(y, X).fit()
model11.summary()

# %%
np.log(df['Gesamtpunkte'])

# %%
# Plotting DV and IV  
 # some filtering for visibility

alt.Chart(df[(df['Einsätze'] > 0) | (df['Marktwert'] > 1000000)]).mark_point().encode(
    x='Gesamtpunkte',
    y='Marktwert',
    color='team',
    shape = 'Position',
    #size = 'Einsätze',
    tooltip=['Spieler','Gesamtpunkte', 'Marktwert', 'team']
).interactive()

# %%


df[(df['Einsätze'] > 0) | (df['Marktwert'] > 1000000)].boxplot(column = 'Marktwert', by = 'team')
plt.xticks(rotation=90)
# %%
alt.Chart(df[(df['Einsätze'] > 0) | (df['Marktwert'] > 1000000)]).mark_point().encode(
    x='Ø–Note Gesamt',
    y='Marktwert',
    color='team',
    shape = 'Position',
    size = 'Gesamtpunkte',
    tooltip=['Spieler','Gesamtpunkte', 'Marktwert', 'team', 'Ø–Note Gesamt']
).interactive()
# %%
df['Gesamtpunkte_avg'] = df['Gesamtpunkte'] - df['Gesamtpunkte'].mean()
df['Gesamtpunkte_stand'] = (df['Gesamtpunkte'] - df['Gesamtpunkte'].mean()) / df['Gesamtpunkte'].std()
# %%
alt.Chart(df[(df['Einsätze'] > 0) | (df['Marktwert'] > 1000000)]).mark_bar().encode(
    x=alt.X('Spieler', sort='-y'),
    y='Gesamtpunkte_stand',
    color='team',
    #shape = 'Position',
    #size = 'Gesamtpunkte',
    tooltip=['Spieler','Gesamtpunkte', 'Marktwert', 'team', 'Ø–Note Gesamt']
).interactive()
# %%
# %%
