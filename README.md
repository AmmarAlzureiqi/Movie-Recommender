# Movie Recommender

## Authors

- Ammar Alzureiqi - ammar3@illinois.edu
- Ahmed Elfarra - ahmedse2@illinois.edu

Website link: [Movie Recommender](https://movie-recommender-aa.streamlit.app/)

## Project Overview

This project involves creating a movie recommender website using Python and Streamlit. The recommender system is divided into two main systems:

1. **System 1 - Genre-based Recommender**
2. **System 2 - Collaborative Filtering Recommender**

## System 1: Genre-based Recommender

The genre-based recommender system suggests movies based on the selected genre. The top movies in each genre are determined based on a weighted average rating.

### Weighted Rating Formula

![Example Image](images/formula.png)


Where:
- **mean_ratings** is the mean of the ratings for the movie.
- **count** is the number of reviews for this movie.
- **median** is the median number of reviews for movies in this genre.

This formula helps in dealing with movies that receive only a few high-point reviews.

### Implementation Overview

1. **Data Loading**: Movies and ratings data are loaded from `.dat` files.
2. **Data Preprocessing**: The data is merged and aggregated to compute mean ratings, counts, and median counts.
3. **Weighted Ratings Calculation**: The weighted average ratings are computed for each movie.
4. **Genre Selection**: Users can select a genre from a predefined list.
5. **Display Top Movies**: The top 10 movies in the selected genre are displayed with their images and ratings.

## System 2: Collaborative Filtering Recommender

The collaborative filtering system suggests movies based on user ratings. Users rate some movies, and recommendations are generated using Item-Based Collaborative Filtering (IBCF).

### Implementation Overview

1. **Data Loading**: Movies data is loaded.
2. **User Rating Collection**: Users rate a set of displayed movies.
3. **Generate Recommendations**: Using the user's ratings, the system generates a list of recommended movies.
4. **Display Recommendations**: Recommended movies are displayed with their titles and genres.

## Conclusion

The Movie Recommender Website provides two different recommendation systems:
- **Genre-based Recommender**: Suggests movies based on selected genres using weighted average ratings.
- **Collaborative Filtering Recommender**: Provides personalized movie recommendations based on user ratings.

Both systems leverage Streamlit for an interactive and user-friendly web interface, enabling users to easily discover new movies based on their preferences and ratings.
