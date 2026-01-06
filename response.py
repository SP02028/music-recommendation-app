import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

def get_app_response(recommended_songs, recommended_artists):
    if recommended_songs is not None:
        st.markdown("### Recommended Songs:")
        df = pd.DataFrame({
            "Track": recommended_songs,
            "Artist": recommended_artists
        })
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)
