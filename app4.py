import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Page config
st.set_page_config(page_title="Mood Music 🎵", layout="centered")

# 🎨 CUSTOM CSS (THIS IS THE MAGIC)
st.markdown("""
<style>

.stApp {
background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
background-position: center;
}

/* Glass effect container */
.main {
    background-color: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 15px;
}

/* Title */
h1 {
    text-align: center;
    color: #ffffff;
}

/* Input box */
.stTextInput > div > div > input {
    border-radius: 10px;
}

/* Button */
.stButton button {
    background: linear-gradient(45deg, #ff4b2b, #ff416c);
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

/* Song card */
.song-card {
    padding: 12px;
    margin: 10px 0;
    border-radius: 12px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎵 Mood Music Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>Tell your mood, get your vibe 🎧</p>", unsafe_allow_html=True)

# Load data
df = pd.read_csv("song.csv", encoding='latin-1')

df['mood'] = df['mood'].map({
    'sad': 0,
    'happy': 1,
    'calm': 2,
    'energetic': 3
})

# Model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['song'])

model = MultinomialNB()
model.fit(X, df['mood'])

# Input
user_input = st.text_input("💭 How are you feeling today?")

# Button
if st.button("✨ Get My Playlist"):

    if user_input.strip() == "":
        st.warning("⚠️ Please tell me your mood first")
    else:
        user_input = user_input.lower().strip()

        mood_map_reverse = {
            'sad': 0,
            'happy': 1,
            'calm': 2,
            'energetic': 3
        }

        if user_input in mood_map_reverse:
            result = [mood_map_reverse[user_input]]
        else:
            st.warning("Please enter: sad, happy, calm, energetic")
            st.stop()
        mood_map = {0: '😔 Sad',1: '😄 Happy',2: '😌 Calm',3: '⚡ Energetic'}

        detected_mood = mood_map[result[0]]

        st.markdown("---")
        st.markdown(f"<h3 style='color:white;'>🎭 Detected Mood: {detected_mood}</h3>", unsafe_allow_html=True)

        recommended_songs = df[df['mood'] == result[0]]

        st.markdown("<h3 style='color:white;'>🎶 Your Playlist</h3>", unsafe_allow_html=True)

        for song in recommended_songs['song']:
            st.markdown(f"<div class='song-card'>🎵 {song}</div>", unsafe_allow_html=True)
