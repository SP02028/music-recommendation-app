import os
import urllib.request
import streamlit as st

def download_data():
    """Download data files if they don't exist"""
    
    data_files = {
        'data_with_most_lyrics.csv': 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/data_with_most_lyrics.csv',
        'spotify_data_urls.csv': 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/spotify_data_urls.csv'
    }
    
    for filename, url in data_files.items():
        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            try:
                # Add headers to avoid 403 Forbidden
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"✓ {filename} downloaded successfully")
            except Exception as e:
                print(f"✗ Error downloading {filename}: {e}")
                raise
        else:
            print(f"✓ {filename} already exists")

if __name__ == "__main__":
    download_data()
