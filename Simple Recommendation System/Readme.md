# Movie Recommendation System

## Project Overview
This project implements a simple movie recommendation system that suggests movies to users based on their preferences. It uses both collaborative filtering and content-based filtering techniques to provide personalized movie recommendations.

## Features
1. Collaborative Filtering: Recommends movies based on user similarity.
2. Content-Based Filtering: Recommends movies similar to those the user has highly rated.
3. Interactive Rating System: Allows users to rate movies and immediately see how it affects their recommendations.
4. Movie Suggestions: Helps users find movies by suggesting titles based on partial input.

## Requirements
- Python 3.7+
- pandas
- numpy
- scipy
- scikit-learn

## Dataset
This project uses the MovieLens Small Dataset. Make sure you have the following files in your project directory:
- `movies.csv`: Contains movie information (movieId, title, genres)
- `ratings.csv`: Contains user ratings (userId, movieId, rating, timestamp)

## Installation
1. Clone this repository or download the script.
2. Install the required libraries:
   ```
   pip install pandas numpy scipy scikit-learn
   ```
3. Download the MovieLens Small Dataset and place `movies.csv` and `ratings.csv` in the same directory as the script.

## Usage
1. Run the script:
   ```
   python movie_recommender.py
   ```
2. Enter your user ID when prompted (you can use any number, new users are automatically handled).
3. Rate some movies when prompted. You can enter partial movie titles, and the system will suggest matching movies.
4. After rating movies, the system will provide recommendations based on collaborative filtering and content-based filtering.
5. You can continue rating more movies to refine your recommendations.

## How It Works
1. Collaborative Filtering: This method finds users similar to you based on rating patterns and recommends movies that these similar users have rated highly.
2. Content-Based Filtering: This method recommends movies similar to the ones you've rated highly, based on movie features (in this case, genres).
3. The system combines both methods to provide a diverse set of recommendations.

## Future Improvements
- Implement a web-based user interface
- Add more advanced recommendation algorithms
- Incorporate more features like movie descriptions or user demographics
- Optimize for larger datasets

## Acknowledgements
This project uses the MovieLens dataset:
F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872

## Note for Beginners
While this system uses some advanced concepts and libraries, it serves as an excellent learning resource for understanding how recommendation systems work. As you continue to learn and grow, you'll be able to understand and modify more aspects of this code.
