import streamlit as st
import pickle
import pandas as pd
import requests



@st.cache_data
def fetch_poster(movie_id):
    api_key = '65384d83a5affde18e307dd56035e762'

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    try:
        response = requests.get(url, timeout=5)  # ✅ FIX
        data = response.json()

        poster_path = data.get('poster_path')  # ✅ SAFE

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500"

    except:
        return "https://via.placeholder.com/500"
# @st.cache_data
# def fetch_poster(movie_id):
#     import requests
    # api_key = 'https://api.themoviedb.org/3/movie/{}?api_key=65384d83a5affde18e307dd56035e762'
    #
    # url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    # data = requests.get(url).json()
    #
    # poster_path = data['poster_path']
    # return "https://image.tmdb.org/t/p/w500/" + poster_path
# def fetch_poster(movie_id):
#     response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=65384d83a5affde18e307dd56035e762'.format(movie_id))
#     data = response.json()
#
#     return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies = pickle.load(open('movies.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox('Select your Movie', movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


