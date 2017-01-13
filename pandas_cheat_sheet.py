
import pandas as pd

<<<<<<<<<<<<<<<<<<CREATE DATA FRAME>>>>>>>>>>>>>>>>>>>
#how to create a dataframe from scratch 
df = pd.DataFrame({'a':['Small', 'Medium', 'High'], 'b':['kinda', 'sorta', 'maybe']})


<<<<<<<<<<<<<<<<<<IMPORT>>>>>>>>>>>>>>>>>>>
#read csv with proper encoding
df = pd.read_csv('file_name.csv', encoding="ISO-8859-1")


<<<<<<<<<<<<<<<<<<COLUMNS>>>>>>>>>>>>>>>>>>>
#show column names
df.columns.values
#column names as a list
list(df.columns.values)
#show header
df.head

<<<<<<<<<<<<<<<<<<SORTING>>>>>>>>>>>>>>>>>>>
#sort col least to greatest
df.sort('pass_completions', ascending=True)
#sorts column G greatest to least, False(0=False/1=True)
df.sort('col', ascending=[0])
#sorting columns by multiple values 
df.sort(['col', 'col2'], ascending=[False, False])

#create a new dataframe from columns in existing data frame 
df_cols = df[['player_name','position']].copy()
df_cols = df[['player_name', 'position']]


<<<<<<<<<<<<<<<<<SELECTING COLUMN VALUES BASED ON CONDITIONS>>>>>>>>>>>>>>>>>>>
#indexing a column based on value then indexing that index 
df.loc[df['position'] == 'tight_end'].iloc[:2]
#deletes values in col1 of data frame test that are less than 5 
df.ix[~(df['games_played'] < 5)]
#selects values in col that are <= 5 
df.ix[df['games_played'] <= 5]
#gives the number of 5's in 'col' column
len(df.loc[df['games_played'] == '5'])
#selects multiple columns based on multiple conditions
df.ix[(df['FOLLOWERS COUNT:'] < 1000) & (df['FRIENDS COUNT:'] < 1000) & (df['RETWEET COUNT:'] == 0)]



<<<<<<<<<<<<<<<<<<FIND AND REPLACE>>>>>>>>>>>>>>>>>>>
#finds unique values in col
pd.unique(df[['team_name']].values.ravel())
#find and replace column values -- whats the difference?
df['team_name'].replace('arIzOnA', 'Arizona',inplace=True)
#find and replace column values -- whats the difference?
df['Month'].replace([1,2],['January','February'], inplace=True)
#replace column names  <<<<-DEPRECATED??
df.rename(columns={'orig_name': 'new_name'}, inplace=True)
#format column values -- i.e. removes the space between first and last name 
df['player_name'].str.replace(" ", "")



<<<<<<<<<<<<<<<<<<COMBINING DATA FRAMES BASED ON COLUMN VALUES>>>>>>>>>>>>>>>>>>>
#select certain values from a row ...
df1 = df.loc[df['Position'] == 'RB']
df2 = df.loc[df['Position'] == 'QB']
df3 = df.loc[df['Position'] == 'WR']
#store each df as a list(can be indexed like a list too)...
frames = [df1, df2, df3]
#merge data frames vertically -- "stack them on top of one another"...
new_df = pd.concat(frames)
#drop all NaN's in rows 
new_df.dropna()

