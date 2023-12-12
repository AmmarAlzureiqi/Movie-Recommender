import streamlit as st
import numpy as np
import pandas as pd
from myfuns import genres, get_displayed_movies, get_popular_movies, get_recommended_movies, get_movie_image_url, get_top_movies, rating_to_stars, myIBCF
from PIL import Image

# Set up the page
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Sidebar
st.sidebar.header("Movie Recommender")
page = st.sidebar.radio("Navigation", ["System 1 - Genre", "System 2 - Collaborative"])

# Main content
st.title(page)

if page == "System 1 - Genre":
    movies_columns = ['MovieID', 'Title', 'Genres']
    movies = pd.read_csv('data/movies.dat', sep='::', engine='python', names=movies_columns, encoding='ISO-8859-1')

    ratings_columns = ['UserID', 'MovieID', 'Rating', 'Timestamp']
    ratings = pd.read_csv('data/ratings.dat', sep='::', engine='python', names=ratings_columns, encoding='ISO-8859-1')

    # Define the list of genres to select from
    GENRES = [
        'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
        'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
    ]

    # Load and preprocess the data
    @st.cache_data
    def load_data():
        # Merge movies and ratings
        data = pd.merge(ratings, movies, on='MovieID')
        
        # Compute the average rating, count of ratings, and median number of ratings for each movie
        movie_stats = data.groupby('MovieID').agg({'Rating': ['mean', 'count']})
        movie_stats.columns = ['mean', 'count']

        # Compute the median number of ratings per genre
        genre_median_ratings = data.groupby('Genres')['Rating'].count().median()

        # Calculate the weighted average ratings using the formula
        movie_stats['weighted_mean'] = (
            (movie_stats['mean'] * movie_stats['count']) / (movie_stats['count'] + genre_median_ratings)
        )
        
        return movies, movie_stats


    movies, movie_stats = load_data()


    # Streamlit app layout
    st.title('Movie Recommender System')

    # Sidebar for genre selection
    genre = st.sidebar.selectbox("Select your favorite movie genre", GENRES)
    # Function to convert rating to star symbols


    # Display the top movies for the selected genre in a grid layout
    if genre:
        st.header(f"Top 10 Highly-Rated Movies in {genre}")
        top_movies = get_top_movies(genre, movie_stats, movies)

        # Number of columns in the grid (e.g., 2, 3, 4, etc.)
        num_cols = 3

        # Create rows of columns (containers)
        rows = [st.container() for _ in range(0, len(top_movies), num_cols)]
        grid_cols = [row.columns(num_cols) for row in rows]

        for index, (_, row) in enumerate(top_movies.iterrows()):
            # Determine the position of the current movie in the grid
            col_index = index % num_cols
            row_index = index // num_cols

            movie_id = row['MovieID']
            title = row['Title']
            rating = row['weighted_mean']
            image_url = get_movie_image_url(movie_id)

            # Display movie in the appropriate grid cell
            with grid_cols[row_index][col_index]:
                st.image(image_url, width=150)  # Adjust the width as needed
                st.write(f"{title}")
                st.write(f"Rating: {rating_to_stars(rating)} ({rating:.1f})")
else:
    movies = get_displayed_movies()
    st.header("Rate some movies below to")

    movies_columns = ['movie_id', 'title', 'genres']
    movies2 = pd.read_csv('data/movies.dat', sep='::', engine='python', names=movies_columns, encoding='ISO-8859-1')
    movies2['movie_id'] = movies2['movie_id'].astype(int)

    # Create a dictionary to store user ratings with default values set to 0
    user_ratings = {movie['movie_id']: np.nan for _, movie in movies.iterrows()}

    # Calculate the number of rows needed for a 2-column grid
    num_rows = len(movies)

    # Iterate over the rows and columns of the grid
    for idx in range(num_rows):
        col1, col2 = st.columns(2)

        if idx < len(movies):
            movie = movies.iloc[idx]

            # Display movie image beside the star rating
            img = Image.open(f"movies_folder/{movie['movie_id']}.jpg")
            col1.image(img, width=100, caption=movie['title'])

            # Add a star rating for each movie
            rating = col2.number_input(f"Rate {movie['title']}", 0, 5, key=f"rating_{movie['movie_id']}")
            
            # Update the user_ratings dictionary
            user_ratings[movie['movie_id']] = rating

    get_recommendations_button = st.button("Get recommendations 😍", key="button-recommend")

    if get_recommendations_button:
        # Display a loading spinner while recommendations are being calculated
        with st.spinner("Calculating recommendations..."):
            # Use user_ratings dictionary to get recommendations
            recommendations = get_recommended_movies(user_ratings)
            st.header("Your recommendations")

            full_list = list(user_ratings.values()) + [np.nan] * (3706 - len(list(user_ratings.values())))
            full_list = pd.Series(full_list)
            templist = myIBCF(full_list)
            cleaned_list = [int(index[1:]) for index in templist]
            tempmovies = movies2[movies2['movie_id'].isin(cleaned_list)]

            tempmovies.loc[:, 'movie_id'] = pd.Categorical(tempmovies['movie_id'], categories=cleaned_list, ordered=True)
            tempmovies = tempmovies.sort_values(by='movie_id').reset_index(drop=True)
            st.table(tempmovies)

    else:
        st.write("Rate some movies and press the 'get recommendations' button")








# Footer
st.sidebar.markdown("---")
st.sidebar.text("Ammar Alzureiqi and Ahmed Elfarra")



