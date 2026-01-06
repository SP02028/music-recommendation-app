import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import os
import urllib.request

# Ensure data files are available
def download_data_if_needed():
    data_files = {
        'data_with_most_lyrics.csv': 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/data_with_most_lyrics.csv',
        'spotify_data_urls.csv': 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/spotify_data_urls.csv'
    }
    for filename, url in data_files.items():
        if not os.path.exists(filename):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                raise RuntimeError(f"Failed to download {filename}: {e}")

download_data_if_needed()

# Music data
music_data = pd.read_csv('data_with_most_lyrics.csv')
music_data = music_data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
music_data['lyrics'] = music_data['lyrics'].str.replace('\n', ' ')
available_songs = music_data["track_name"] + ', ' + music_data["artist_name"]
available_songs = available_songs.tolist()

# Past music data
past_data = pd.read_csv('spotify_data_urls.csv')

def find_title_from_index(index):
    return music_data["track_name"][index]

def find_artist_from_index(index):
    return music_data["artist_name"][index]

def find_index_from_title(track_name):
    return music_data.index[music_data.track_name == track_name].values[0]

def top_song_recs(genre2, K, method='track_popularity'):
  # separating genre values
  separated_genres = separate_values('genres')

  # segmenting data based on chosen genre
  genre_tracks = None
  if genre2 != None:
    genre_tracks = separated_genres.loc[separated_genres['genres'] == genre2]

    if method == 'hit_prediction':
      X = past_data[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]
      y = past_data[['Label']]
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

      lr = LogisticRegression()
      lr.fit(X_train,y_train)

      X_new = genre_tracks[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]
      genre_tracks['hit_prediction'] = lr.predict(X_new)

      genre_hits = genre_tracks.loc[genre_tracks['hit_prediction'] == 1][:K]
    else:
      genre_hits = genre_tracks.sort_values('track_popularity', ascending=False)[:K]
    return genre_hits['track_name'].tolist(), genre_hits['artist_name'].tolist()
  return None, None

def parse_string_into_list(string):
  return string[1:len(string)-1].split(', ')

def separate_values(column):
  mdata = music_data.copy()
  mdata[column] = mdata.apply(lambda row: parse_string_into_list(row[column]), axis=1)
  mdata.head()

  mdata = mdata.explode(column)
  return mdata
