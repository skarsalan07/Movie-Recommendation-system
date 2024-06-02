import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

# CSS for styling
st.markdown("""
<style>
body {
    background-color: #121212; /* Dark background color */
    color: #FFFFFF;
}

.sidebar .sidebar-content {
    background-color: rgba(0, 0, 0, 0.8);
    border-radius: 10px;
}

.stButton>button {
    background-color: #FF6347;
    color: #FFFFFF;
    border-radius: 5px;
}

.stButton>button:hover {
    background-color: #FF4500;
}

.stSelectbox {
    color: #FFFFFF;
}

.stTextInput>div>div>input {
    color: #FFFFFF;
}

.stTextInput>div>div>input::placeholder {
    color: #FFFFFF;
}

.stText {
    color: #FFFFFF;
}

.footer {
    position: fixed;
    bottom: 10px;
    right: 10px;
    color: #FFFFFF;
}

.footer a {
    color: #FF4500; /* Link color */
    text-decoration: none;
    transition: color 0.3s;
}

.footer a:hover {
    color: #FFFFFF; /* Hover color */
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.title('🎬 Movie Match Maker')
st.markdown("""
<h2>Welcome to the Movie Recommendation System!</h2>
<h3>Choose movies from dropdown we will recommend you.</h3>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b00ee225f11fac3a7056e51e968ffc94')
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

def combine_similarity_pkl(similarity_pkl1, similarity_pkl2):
    similarity1 = pickle.load(open(similarity_pkl1, 'rb'))
    similarity2 = pickle.load(open(similarity_pkl2, 'rb'))
    combined_similarity = np.concatenate((similarity1, similarity2), axis=0)
    return combined_similarity

def recommend(movie, similarity_matrix, movies_df):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]]['id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Sidebar for user input
st.sidebar.header('Select a Movie')
selected_movie = st.sidebar.selectbox("Choose a movie you like:", movies['title'].values)

# Combine similarity matrices
combined_similarity = combine_similarity_pkl('similarity.pkl', 'similarity1.pkl')

if st.sidebar.button('Show Recommendations'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie, combined_similarity, movies)

    # Display recommended movies in a neat layout
    num_cols = 2
    num_recommended = len(names)
    num_rows = (num_recommended + num_cols - 1) // num_cols
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx, col in enumerate(cols):
            movie_idx = row * num_cols + col_idx
            if movie_idx < num_recommended:
                col.image(posters[movie_idx], use_column_width=True)
                col.text(names[movie_idx])
            else:
                col.empty()  # Leave the column empty if there are no more recommended movies

# Footer
st.markdown("""
---

<div class="footer">
    <a href="https://arsalanportfolio7.netlify.app/" target="_blank">Discover more projects by the developer</a>
    <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
    <span>🚀</span>
</div>
""", unsafe_allow_html=True)
