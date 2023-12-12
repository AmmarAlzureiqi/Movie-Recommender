import pandas as pd
import numpy as np
import requests
from PIL import Image
import heapq

movies_columns = ['movie_id', 'title', 'genres']
movies = pd.read_csv('data/movies.dat', sep='::', engine='python', names=movies_columns, encoding='ISO-8859-1')
movies['movie_id'] = movies['movie_id'].astype(int)
print(movies['movie_id'])

genres = list(
    sorted(set([genre for genres in movies.genres.unique() for genre in genres.split("|")]))
)

def get_displayed_movies():
    return movies.head(50)

def get_recommended_movies(new_user_ratings):
    return movies.head(10)

def get_popular_movies(genre: str):
    if genre == genres[1]:
        return movies.head(10)
    else: 
        return movies[10:20]

def get_movie_image_url(movie_id):
    img = Image.open(f"movies_folder/{movie_id}.jpg")
    return img

# Function to get top movies for the selected genre
def get_top_movies(genre, movie_stats, movies, top_n=10):
    # Filter movies by the selected genre
    genre_movies = movies[movies['Genres'].str.contains(genre)]
    
    # Join with the movie stats
    genre_movies_stats = genre_movies.join(movie_stats, on='MovieID')
    
    # Filter movies with more than a threshold of ratings to avoid movies with few high ratings
    popular_movies = genre_movies_stats[genre_movies_stats['count'] > 100]
    
    # Get the top N movies by average rating
    top_movies = popular_movies.sort_values(by='mean', ascending=False).head(top_n)
    return top_movies

def rating_to_stars(rating):
    full_stars = int(rating)
    half_star = "⭐" if rating - full_stars >= 0.5 else ""
    return '⭐' * full_stars + half_star

def myIBCF(newuser):
    S_top30 = pd.read_csv('modified_similarity_matrix.csv')
    S_top30 = S_top30.iloc[:,1:]
    pred = pd.DataFrame(index=range(3706))
    
    pred = []
    for i in range(3706):
        Sl = S_top30.iloc[:, i]
        if sum(np.isfinite(Sl) & np.isfinite(newuser)) == 1:
            result = Sl[(np.isfinite(Sl) & np.isfinite(newuser))] * newuser[(np.isfinite(Sl) & np.isfinite(newuser))]
            result = (1 / np.nansum(Sl[np.isfinite(newuser)])) * result
            pred.append(result.iloc[0])
        elif sum(np.isfinite(Sl) & np.isfinite(newuser)) == 0:
            result = 0
            pred.append(result)
        else:
            result = np.nansum(np.multiply(Sl, newuser))
            result = (1 / np.nansum(Sl[np.isfinite(newuser)])) * result
            pred.append(result)

    nan_positions = np.isnan(newuser)
    
    # Replace NaN values in 'w' with corresponding values from 'pred'
    newuser = [pred_value if is_nan else w_value for w_value, pred_value, is_nan in zip(newuser, pred, nan_positions)]
    
    top_10_indices_and_values = heapq.nlargest(10, enumerate(newuser), key=lambda x: x[1])
    
    # Unpack the result into separate lists of indices and values
    top_10_indices, top_10_values = zip(*top_10_indices_and_values)

    return S_top30.columns[list(top_10_indices)]