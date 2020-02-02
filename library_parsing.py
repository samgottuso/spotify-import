import pandas as pd 
import numpy as np

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
        print(col+'is numeric')
    else:
        #ah we have mixed Dtypes, there's probably some artists with numeric names
        print(col)
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
        q = 'track:'+self.song+' album:'+self.album
        # ' album:'+self.album+' artist'+self.artist
        # +'year'+str(self.year)
        return(q)
    def querify_less(self):
        #TODO if the first query fails, try again with less strict criteria, just need to figure out what that is
        q = 'track:'+self.song
        return(q)




#visual test to confirm
#TODO make this into a function
beatles_songs = all_songs.loc[all_songs['Artist']=='The Beatles']

for i,row in beatles_songs.head().iterrows():
    test_obj = spotipy_query(row)
    # obj_query = test_obj.querify_less()
    # print(obj_query)
    # results=sp.search(q=obj_query,limit=1)
    # print(results)
    strict_obj_query = test_obj.querify_strict()
    results2=sp.search(q=strict_obj_query,limit=1)
    print(results2)
