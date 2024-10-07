import pickle
import streamlit as st
import requests


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d1b737887ce995840cac2367549ac50a&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit app header
st.header('Movie Recommender System')


# Function to download files
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        st.error(f"Failed to download {filename}")

similarity_url = 'https://gdrive-s3-bucket.s3.ap-south-1.amazonaws.com/similarity.pkl'
movie_list_url = 'https://gdrive-s3-bucket.s3.ap-south-1.amazonaws.com/movie_list.pkl'

download_file(similarity_url, 'similarity.pkl')
download_file(movie_list_url, 'movie_list.pkl')

# Load the movie list and similarity matrix from the downloaded pickle files
with open('movie_list.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations button
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)

