import streamlit as st
import pickle 
import pandas as pd 
import requests

st.title('Movie Recommendation System ')

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b00ee225f11fac3a7056e51e968ffc94'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
    # Finding index which you are searched 
    movie_index = movies[movies['title'] == movie].index[0]
    # Distance between movie which you have searched and other movies to suggest
    distances = similarity[movie_index]
    # We convert array into tuple and sort it into desc order because the similarity value is going at the end and chosen 5 movies 
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']  # Assuming the movie ID column is named 'id'
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

selected_movie = st.selectbox("Select a movie", movies['title'].values)
similarity = pickle.load(open('similarity.pkl', 'rb'))

if st.button('Search Similar Movies'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, (name, poster) in enumerate(zip(names, posters)):
        with cols[i]:
            st.text(name)
            st.image(poster)
