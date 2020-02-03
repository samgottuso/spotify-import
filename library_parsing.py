import pandas as pd 
import numpy as np
import sqlite3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())



all_songs = pd.read_csv('Music.txt',sep='\t',header=0,engine='python')


#triming and renaming columns

first_range = list(range(0,5))

second_range = [7,12]
total_range = first_range + second_range

all_songs = all_songs.iloc[:,total_range]

# all_songs.columns = ['Name','Artist','Composer','Album','Grouping','Genre','Time','Year']

#lambda apply function to change all of the spaces



for col in all_songs.columns:
    #lazy non-int/float condition
    if all_songs[col].dtype in [int,float]:
        pass
            else:
        #ah we have mixed Dtypes, there's probably some artists with numeric names
        all_songs[col] = all_songs[col].astype(str)
        #so they're already changing the spaces in the spotipy.search method
        # all_songs[col] = all_songs[col].apply(lambda x:x.replace(' ','%20'))

#while we're converting dtypes

all_songs['Year'] = all_songs['Year'].astype(str,errors='ignore')

all_songs['Year'] = all_songs['Year'].str.replace('.0','')

print(len(all_songs['Artist']))

all_songs = all_songs.dropna()

print(len(all_songs['Artist']))

#Create class object to pass to the search

class spotipy_query():
    def __init__(self,row):
        self.song = row['Name'].lower()
        self.artist = row['Artist'].lower()
        self.album = row['Album'].lower()
        self.year = row['Year']
    
    def querify_strict(self):
        q = 'track:'+self.song+' album:'+self.album+' artist:'+self.artist
        # ' album:'+self.album+' artist'+self.artist
        # +'year'+str(self.year)
        return(q)
    def querify_less(self):
        #TODO if the first query fails, try again with less strict criteria, just need to figure out what that is
        q = 'track:'+self.song+' artist:'+self.artist
        return(q)
    def failed_to_db(self,sql_statement):
        params_dict = {'song':self.song,'artist':self.artist,'album':self.album,'year':self.year}
        #create this above when the db gets spun up.
        liteCursor.execute(sql_statement,params_dict)
        



query_less_list = []
query_strict_list = []
#visual test to confirm
#TODO make this into a function
beatles_songs = all_songs.loc[all_songs['Artist']=='The Beatles']

for i,row in all_songs.sample(1000).iterrows():
    test_obj = spotipy_query(row)
    obj_query = test_obj.querify_less()
    results=sp.search(q=obj_query,limit=1)
    if results['tracks']['items']:
        query_less_list.append(results['tracks']['items'])
    strict_obj_query = test_obj.querify_strict()
    results2=sp.search(q=strict_obj_query,limit=1)
    if results2['tracks']['items']:
        query_strict_list.append(results2['tracks']['items'][0]['id'])

    #Test to ensure that we get enough results for the strict list
#number found by strict
print('strict list found')
print(len(query_strict_list))
#number found by less strict
print('less strict list found')
print(len(query_less_list))

#On the first 1000 sample the less strict found 89 records while the more strict found 597
#TODO test out different cominbations to figure out what returns the most

#TODO gonna have to accept that there's not gonna be full matches for everything two options I can think of.
# 1. Spin up a sqllite db and write the exceptions there, and then query for manual addition/another approach
# 2. Run through the full list in the playlist and do list comprehension to figure out which didn't make it to the playlist