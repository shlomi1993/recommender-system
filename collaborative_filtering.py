# Shlomi Ben-Shushan


import pandas as pd
import numpy as np
import heapq
from sklearn.metrics.pairwise import pairwise_distances


class collaborative_filtering:

    def __init__(self):
        """
        Collaborative-Filtering object constructor.
        Initialize attributes that needed to be shared with different functions.
        """
        self.unique_users = []
        self.unique_movies = []
        self.userId_to_index = {}   # a mapper from user-id to serial index.
        self.movieId_to_index = {}  # a mapper from movie-id to serial index.
        self.movieId_to_title = {}  # a mapper from movie-id to movie title.
        self.user_based_matrix = []
        self.item_based_metrix = []

    def create_fake_user(self, rating):
        """
        This method adds new fake user to the given ratings list.
        User's character is determined by the ratings he gives.

        :param rating: the information from ratings.csv file.
        :return: concatenation between the given ratings and new fake user data.
        """
        uid = 283238  # according to the instructions.
        n_ratings = len(rating)
        new_indexes = [n_ratings + i for i in range(5)]
        new_data = {
            'userId': [uid, uid, uid, uid, uid],
            'movieId': [33794, 153, 592, 595, 596],
            'rating': [5.0, 4.5, 5.0, 1.5, 0.5]
        }
        self.userId_to_index[uid] = len(self.unique_users)
        self.unique_users.append(uid)
        return pd.concat([rating, pd.DataFrame(new_data, index=new_indexes)])

    def create_pred_matrix(self, data, user_based):
        """
        This function creates user-based prediction matrix if user_based is True
        and item-based prediction matrix if it is False.

        :param data: a tuple of ratings data and movies data.
        :param user_based: a boolean that tells which matrix to create.
        :return:
        """

        # Get input.
        ratings, movies = data

        # Update object's attributes.
        self.unique_users = ratings['userId'].unique().tolist()
        self.unique_users.sort()
        self.unique_movies = ratings['movieId'].unique().tolist()
        self.unique_movies.sort()
        self.userId_to_index = dict(zip(self.unique_users, list(range(len(self.unique_users)))))
        self.movieId_to_index = dict(zip(self.unique_movies, list(range(len(self.unique_movies)))))
        self.movieId_to_title = dict(zip(movies['movieId'], movies['title']))

        # Add a fake user to the data-set.
        ratings = self.create_fake_user(ratings)

        # Create rating difference matrix and calculate mean.
        ratings_pd = ratings.pivot_table(index='userId', columns='movieId', values='rating')
        mean = ratings_pd.mean(axis=1).to_numpy().reshape(-1, 1)
        ratings_diff = ratings_pd.to_numpy() - mean
        ratings_diff[np.isnan(ratings_diff)] = 0

        # Calculate the required prediction matrix (depending on user_based boolean).
        if user_based:
            user_similarity = 1 - pairwise_distances(ratings_diff, metric='cosine')
            pred = mean + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T
        else:
            item_similarity = 1 - pairwise_distances(ratings_diff.T, metric='cosine')
            pred = mean + ratings_diff.dot(item_similarity) / np.array([np.abs(item_similarity).sum(axis=1)])

        # Reset user rated movies in the prediction matrix.
        for u, m in zip(ratings['userId'], ratings['movieId']):
            i = self.userId_to_index[u]
            j = self.movieId_to_index[m]
            pred[i][j] = 0
        return pred

    def create_user_based_matrix(self, data):
        """
        This method creates a user-based matrix by calling create_pred_matrix()
        with user_based=True.

        :param data: a tuple of ratings data and movies data.
        :return: None. Update user_based_matrix attribute instead.
        """
        self.user_based_matrix = self.create_pred_matrix(data, user_based=True)

    def create_item_based_matrix(self, data):
        """
        This method creates an item-based matrix by calling create_pred_matrix()
        with user_based=False.

        :param data: a tuple of ratings data and movies data.
        :return: None. Update item_based_metrix attribute instead.
        """
        self.item_based_metrix = self.create_pred_matrix(data, user_based=False)

    def predict_movie_ids(self, user_id, k, is_user_based=True):
        """
        This method predicts the "k" movies recommended to the user "user_id"
        according to the user-based-matrix if "is_user_based" is True or to the
        item-based-matrix if it is False. This method returns the movies as
        tuples of movie-ID and match-score for the given user.

        :param user_id: a number that represents a user.
        :param k: the number of predictions needed
        :param is_user_based: a boolean that tells which matrix to use.
        :return: list of k most recommended movies as tuples as described above.
        """

        # Choose matrix.
        matrix = self.user_based_matrix if is_user_based else self.item_based_metrix

        # Extract the row refers to the user_id.
        row = matrix[self.userId_to_index[int(user_id)]]

        # Create a list of tuples of movieId and match-score-for-user.
        recommendations = list(zip(self.unique_movies, row))

        # Sort the list by match-score.
        recommendations.sort(reverse=True, key=lambda tup: tup[1])

        # Return the k first tuples.
        return [tup for tup in recommendations[:k]]

    def predict_movies(self, user_id, k, is_user_based=True):
        """
        This is the required function according to the instructions. It returns
        a list of the k most recommended movies. It uses the previous method and
        then converts each movie ID to its title. Then it creates a message that
        lists the recommended movies as string and returns it.

        :param user_id: a number that represents a user.
        :param k: the number of predictions needed
        :param is_user_based: a boolean that tells which matrix to use.
        :return: a string of the k most recommended movies.
        """
        recommendations = self.predict_movie_ids(user_id, k, is_user_based)
        msg = f'Top-{k} recommendations for user {user_id}:\n'
        for i in range(k):
            mid, match = recommendations[i]
            title = self.movieId_to_title[mid]
            match = str(round((100 * match) / 5.0, 2)) + '%'
            msg += f'{i + 1}) {title} - with match score of {match}.\n'
        return msg[:-1]
