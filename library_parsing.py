import pandas as pd 
import numpy as np
import sqlite3
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#importing local class
from spotipy_query import spotipy_query,search_loop

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

#converting dtypes
str_list = ['Name','Artist','Album','Year']

for col in str_list:
    all_songs[col] = all_songs[col].astype(str,errors='ignore')

all_songs['Year'] = all_songs['Year'].str.replace('.0','')

all_songs['Name'] = all_songs['Name'].str.replace("'",'')

all_songs['Name'] = all_songs['Name'].str.replace(",",'')


#subbing out stuff that's enclosed in ()s

all_songs['Name'] = all_songs['Name'].apply(lambda x: re.sub('[(].+[)]','',x))

print(all_songs['Name'])

        
returned_list = []

for i,row in all_songs.iterrrows():
    search_loop(row,playlist='',client=sp,out_list=returned_list,insert_statement=failed_to_find,db=missing_db)
