import pandas as pd 
import numpy as np
import sqlite3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#importing local class
from spotipy_query import spotipy_query

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())



all_songs = pd.read_csv('Music.txt',sep='\t',header=0,engine='python')

with open('missing_track_insert.sql') as f:
    failed_to_find = f.read()

missing_db = sqlite3.connect('spotipy.db')


#triming and renaming columns

first_range = list(range(0,5))

second_range = [7,12]
total_range = first_range + second_range

all_songs = all_songs.iloc[:,total_range]

#while we're converting dtypes

print(all_songs)

str_list = ['Name','Artist','Album','Year']

for col in str_list:
    all_songs[col] = all_songs[col].astype(str,errors='ignore')

all_songs['Year'] = all_songs['Year'].str.replace('.0','')

# TODO looks like a lot of songs with apostrophes,back slashes or () are failing, we can write those out.
        
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
    else:
        print(test_obj.song+' failed')
        test_obj.failed_to_db(failed_to_find,missing_db,'less_strict')
    
    strict_obj_query = test_obj.querify_strict()
    results2=sp.search(q=strict_obj_query,limit=1)
    if results2['tracks']['items']:
        query_strict_list.append(results2['tracks']['items'][0]['id'])
    else:
        test_obj.failed_to_db(failed_to_find,missing_db,'more_strict')

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