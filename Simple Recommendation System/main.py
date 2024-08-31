import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')


# Collaborative Filtering
def collaborative_filtering(user_id, n_recommendations=10):
    # Create a user-item matrix
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    user_item_sparse = csr_matrix(user_item_matrix.values)
    user_similarity = cosine_similarity(user_item_sparse)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Get the user's ratings
    user_ratings = user_item_matrix.loc[user_id]

    # Find similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:11]

    # Get movies rated by similar users but not by the target user
    similar_user_movies = user_item_matrix.loc[similar_users.index]
    unrated_movies = similar_user_movies.columns[user_ratings == 0]

    # Calculate predicted ratings for unrated movies
    predicted_ratings = {}
    for movie in unrated_movies:
        movie_ratings = similar_user_movies[movie]
        weighted_ratings = (movie_ratings * similar_users).sum() / similar_users.sum()
        predicted_ratings[movie] = weighted_ratings

    # Sort and get top N recommendations
    recommendations = sorted(predicted_ratings.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]

    # Get movie titles for recommendations
    recommended_movies = movies[movies['movieId'].isin([movie_id for movie_id, _ in recommendations])]
    recommended_movies = recommended_movies.set_index('movieId')

    return [(recommended_movies.loc[movie_id, 'title'], score) for movie_id, score in recommendations]


# Content-Based Filtering
def content_based_filtering(movie_name, n_recommendations=10):
    # Prepare the genre data
    movies['genres'] = movies['genres'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index of the movie given its title
    idx = movies.index[movies['title'] == movie_name].tolist()
    if not idx:
        return []  # Return empty list if movie not found
    idx = idx[0]

    # Get the pairwise similarity scores for all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores for the most similar movies
    sim_scores = sim_scores[1:n_recommendations + 1]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top n most similar movies
    return [(movies['title'].iloc[i], sim_scores[idx][1]) for idx, i in enumerate(movie_indices)]


def get_user_movie_ratings(user_id):
    user_ratings = ratings[ratings['userId'] == user_id]
    user_movies = pd.merge(user_ratings, movies, on='movieId')
    return user_movies[['title', 'rating']].sort_values('rating', ascending=False)


def print_recommendations(recommendations, title):
    print(f"\n{title}")
    print("-" * len(title))
    for movie, score in recommendations[:5]:
        print(f"{movie}: {score:.2f}")


def add_user_rating(user_id, movie_title, rating):
    global ratings, movies

    # Check if the movie exists
    movie = movies[movies['title'] == movie_title]
    if movie.empty:
        print(f"Movie '{movie_title}' not found.")
        return

    movie_id = movie.iloc[0]['movieId']

    # Check if the rating is valid
    if rating < 0.5 or rating > 5.0 or rating % 0.5 != 0:
        print("Invalid rating. Please use a scale of 0.5 to 5.0, in half-star increments.")
        return

    # Check if the user has already rated this movie
    existing_rating = ratings[(ratings['userId'] == user_id) & (ratings['movieId'] == movie_id)]

    if existing_rating.empty:
        # Add new rating
        new_rating = pd.DataFrame({
            'userId': [user_id],
            'movieId': [movie_id],
            'rating': [rating],
            'timestamp': [pd.Timestamp.now().value // 10 ** 9]  # Current timestamp in seconds
        })
        ratings = pd.concat([ratings, new_rating], ignore_index=True)
        print(f"Added new rating: User {user_id} rated '{movie_title}' as {rating}")
    else:
        # Update existing rating
        ratings.loc[(ratings['userId'] == user_id) & (ratings['movieId'] == movie_id), 'rating'] = rating
        ratings.loc[(ratings['userId'] == user_id) & (
                    ratings['movieId'] == movie_id), 'timestamp'] = pd.Timestamp.now().value // 10 ** 9
        print(f"Updated rating: User {user_id} rated '{movie_title}' as {rating}")


def get_movie_suggestions(partial_title):
    return movies[movies['title'].str.contains(partial_title, case=False, na=False)]['title'].tolist()


# Interactive rating system
def interactive_rating_system(user_id):
    while True:
        movie_title = input("Enter the movie title (or 'q' to quit): ")
        if movie_title.lower() == 'q':
            break

        suggestions = get_movie_suggestions(movie_title)
        if len(suggestions) > 1:
            print("Did you mean:")
            for i, suggestion in enumerate(suggestions[:5], 1):
                print(f"{i}. {suggestion}")
            choice = input("Enter the number of your choice (or press Enter to skip): ")
            if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                movie_title = suggestions[int(choice) - 1]
            else:
                continue
        elif len(suggestions) == 1:
            movie_title = suggestions[0]
        else:
            print("Movie not found. Please try again.")
            continue

        while True:
            try:
                rating = float(input(f"Enter your rating for '{movie_title}' (0.5-5.0): "))
                add_user_rating(user_id, movie_title, rating)
                break
            except ValueError:
                print("Invalid input. Please enter a number between 0.5 and 5.0.")


# Main function to run the recommendation system
def run_recommendation_system():
    print("Welcome to the Movie Recommendation System!")
    user_id = int(input("Please enter your user ID (or a new ID if you're a new user): "))

    print(f"\nHello, User {user_id}!")
    print("Let's start by rating some movies.")
    interactive_rating_system(user_id)

    print("\nBased on your ratings, here are some recommendations:")
    cf_recommendations = collaborative_filtering(user_id)
    print_recommendations(cf_recommendations, "Collaborative Filtering Recommendations:")

    user_top_movies = get_user_movie_ratings(user_id)
    if not user_top_movies.empty:
        random_movie = user_top_movies.sample(1)['title'].values[0]
        print(f"\nGetting content-based recommendations similar to: {random_movie}")
        cb_recommendations = content_based_filtering(random_movie)
        print_recommendations(cb_recommendations, "Content-Based Filtering Recommendations:")
    else:
        print("\nNot enough ratings for content-based recommendations yet.")

    print("\nYou can continue rating more movies to get better recommendations!")
    print("Here are your current ratings:")
    print(get_user_movie_ratings(user_id).to_string(index=False))


# Run the system
if __name__ == "__main__":
    run_recommendation_system()