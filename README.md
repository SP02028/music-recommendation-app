# Music Recommendation App 🎵

A Streamlit web application that provides intelligent music recommendations using machine learning techniques.

## Team
Elisha C, Ethan H, Arush N, Shanaya P, Vasudha P, Enzo R

## Features

This app offers three different recommendation methods:

1. **Popular Songs** - Discover top songs in your favorite genre based on track popularity
2. **Predicted Top Hits** - Use machine learning (Logistic Regression) to predict which songs will be hits in a specific genre
3. **Content-Based Recommendation** - Find songs similar to your favorites based on customizable features:
   - Text features: artist name, track name, album, genres, lyrics
   - Numerical features: popularity, danceability, energy, tempo, and more

## Data

The app uses two datasets that are automatically downloaded from Google Cloud Storage:
- `data_with_most_lyrics.csv` - Main music dataset with lyrics and audio features
- `spotify_data_urls.csv` - Historical Spotify data for hit prediction

## Installation

### Quick Start (Automatic Setup)

1. Clone this repository:
```bash
git clone https://github.com/SP02028/music-recommendation-app.git
cd music-recommendation-app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the app (data downloads automatically on first run):
```bash
streamlit run app.py
```

**That's it!** The data files will be downloaded automatically the first time you run the app.

### Deploy to Streamlit Cloud

This app works out-of-the-box on Streamlit Cloud:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account  
3. Click "New app"
4. Select:
   - Repository: `SP02028/music-recommendation-app`
   - Branch: `main`
   - Main file: `app.py`
5. Click "Deploy"

The data files download automatically during deployment! 🚀

### Manual Data Download (Optional)

If you prefer to download data files manually before running:

**On Mac/Linux:**
```bash
wget 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/data_with_most_lyrics.csv'
wget 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/spotify_data_urls.csv'
```

**On Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/data_with_most_lyrics.csv' -OutFile 'data_with_most_lyrics.csv'
Invoke-WebRequest -Uri 'https://storage.googleapis.com/inspirit-ai-data-bucket-1/Data/AI%20Scholars/Sessions%206%20-%2010%20(Projects)/Project%20-%20Music%20Recommendation/spotify_data_urls.csv' -OutFile 'spotify_data_urls.csv'
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to the URL shown (typically `http://localhost:8501`)

## How It Works

### Popular Songs
- Filters songs by selected genre
- Sorts by track popularity
- Returns top K songs

### Predicted Top Hits
- Uses Logistic Regression trained on historical Spotify hit data
- Features include: danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo
- Predicts which songs are likely to be hits
- Returns top K predicted hits in the selected genre

### Content-Based Recommendation
- Combines text and numerical features into feature vectors
- Uses cosine similarity to find songs most similar to your selection
- Customizable feature selection for personalized recommendations

## Technologies Used

- **Streamlit** - Web application framework
- **scikit-learn** - Machine learning (Logistic Regression, CountVectorizer, cosine similarity)
- **pandas** - Data manipulation
- **numpy** - Numerical computing

## Project Structure

```
music-recommendation-app/
├── app.py                 # Main Streamlit application
├── header.py              # Header component
├── response.py            # Response display component
├── helper.py              # Helper functions for genre-based recommendations
├── contentbased.py        # Content-based recommendation functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## License

This project was created as part of an AI Scholars educational program.