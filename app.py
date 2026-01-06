import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np
import os
from setup import download_data

# Download data files if they don't exist
if not os.path.exists('data_with_most_lyrics.csv') or not os.path.exists('spotify_data_urls.csv'):
    with st.spinner('Downloading data files... This may take a minute on first run.'):
        download_data()

from header import *
from response import *
from helper import *
from contentbased import *

create_header()

def get_song_recs(rec_method, text_features, numerical_features, song, genre, K):
  if rec_method == "Popular Songs":
    return top_song_recs(genre, K)
  elif rec_method == "Predicted Top Hits":
    return top_song_recs(genre, K, method='hit_prediction')
  else:
    if song is not None and song is not []:
      song_vectors = data_formatting(text_features, numerical_features)
      return k_most_similar_songs(song, song_vectors, K)
    return None, None


choice = st.radio("Choose recommendation method: ", ["Popular Songs", "Predicted Top Hits", "Content-Based Recommendation"])
if choice == "Content-Based Recommendation":
  left_column, m1, m2 = st.columns((1,1,1))
  with left_column:
    k = st.slider("Pick a value for K", 1, 20)

  genre = None
  with m1:
    avail_text_feat = ['artist_name', 'track_name', 'album', 'genres', 'lyrics']
    text_features = st.multiselect("Pick your text features!", avail_text_feat)
  with m2:
    avail_num_feat = ['track_popularity', 'year', 'artist_popularity', 'artist_followers', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo','duration_ms', 'time_signature']
    numerical_features = st.multiselect("Pick your numerical features!", avail_num_feat)

  select = st.multiselect("Pick a song!", available_songs, default = None)
  if select == []:
    song = None
  else:
    song = music_data['track_name'][available_songs.index(select[0])]
else:
  left_column, right_column = st.columns(2)
  with left_column:
    k = st.slider("Pick how many songs you want to see!", 1, 20)
  with right_column:
    available_genres = separate_values('genres')['genres'].value_counts().index.tolist()
    select = st.multiselect("Pick a genre!", available_genres)
    if select == []:
      genre = None
    else:
      genre = select[0]
  song = None
  text_features, numerical_features = None, None

recs, artists = get_song_recs(choice, text_features, numerical_features, song, genre, k)
get_app_response(recs, artists)
