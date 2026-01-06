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

def k_most_similar_songs(song, song_vectors, K):
  similaritymatrix = all_similarity(song_vectors)
  song_index = find_index_from_title(song)
  song_similarity = similaritymatrix[song_index]
  
  song_indices = []
  for i in range(0, K):
    currmax = 0
    curridx = None
    for j in range(len(song_similarity)):
      if song_similarity[j] > currmax and j not in song_indices and j != song_index:
          currmax = song_similarity[j]
          curridx = j
    song_indices.append(curridx)
  
  song_names = []
  singers = []
  for s in song_indices:
    song_names.append(find_title_from_index(s))
    singers.append(find_artist_from_index(s))
  return song_names, singers

def combine_features(row, text_features = []):
    combined_row = ''
    for feature in text_features:
      combined_row += str(row[feature])
      combined_row += ' '
    return combined_row[:-1]

def data_formatting(text_features, numerical_features):
  if 'genres' in text_features:
    music_data['genres'] = music_data['genres'].fillna('')
  for feature in text_features:
      music_data[feature] = music_data[feature].fillna('')
  music_data["combined_features"] = music_data.apply(lambda row: combine_features(row, text_features=text_features),axis=1)

  cv = CountVectorizer()
  count_matrix = cv.fit_transform(music_data["combined_features"])

  text_vectors = count_matrix.toarray()
  numerical = music_data[numerical_features].to_numpy()
  song_vectors = np.concatenate((text_vectors, numerical), axis=1)
  return song_vectors

def all_similarity(vectors, sim_metric='cosine'):
  if sim_metric == 'cosine':
    return cosine_similarity(vectors)
  else:
    return -pairwise_distances(vectors, metric=sim_metric)
