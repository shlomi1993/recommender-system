# Shlomi Ben-Shushan


from math import sqrt


K = 10
user_to_movies = {}


def evaluate(test_set, cf, is_user_based, count_hits, threshold):
    """
    This function evaluates a Collaborative Filter using a given test-set. the
    functions Precision@k and ARHR are pretty similar, and the main difference
    between them is how the way on counting the hits. This function the counting
    function in the input count_hits, and by that supports the implementation of
    both Precision@k and ARHR.

    :param test_set: the information given by the file test.csv.
    :param cf: a collaborative-filtering object to evaluate.
    :param is_user_based: a boolean that tells which matrix to use.
    :param count_hits: a function that defines how to count hits.
    :param threshold: this method will refer only to ratings >= threshold.
    :return:
    """

    # Creates a cached mapper from user-id to a list of high rated movies.
    global user_to_movies
    if len(user_to_movies) == 0:
        for u, m, r in zip(test_set['userId'], test_set['movieId'], test_set['rating']):
            if r >= threshold:
                if u in user_to_movies.keys():
                    user_to_movies[u].append(m)
                else:
                    user_to_movies[u] = [m]

    # For each user in the test-set, predict its recommendations and count
    # correlations between them and the high rated movies (by him).
    hits = 0.0
    for u in user_to_movies.keys():
        high_rated_movies = user_to_movies[u]
        recommendations = cf.predict_movie_ids(u, K, is_user_based)
        hits += count_hits(recommendations, high_rated_movies)

    # Return the ratio between the hits and the number of users in the test-set.
    return hits / len(user_to_movies)


def precision_10(test_set, cf, is_user_based=True):
    """
    This function is my implementation of P@k evaluator. It defines count_hits
    function that calculates #hits as 1/k for each hit, and then run evaluate()
    function.

    :param test_set: the information given by the file test.csv.
    :param cf: a collaborative-filtering object to evaluate.
    :param is_user_based: a boolean that tells which matrix to use.
    :return: a float represents the P@k evaluation of the given CF.
    """
    def count_hits(recommendations, high_rated_movies):
        hits = 0
        for m in recommendations:
            if m[0] in high_rated_movies:
                hits += 1
        return hits / K
    val = evaluate(test_set, cf, is_user_based, count_hits, 4.0)
    print("Precision_k: " + str(val))
    return val


def ARHA(test_set, cf, is_user_based=True):
    """
    This function is my implementation of ARHR evaluator. It defines count_hits
    function that calculates #hits as 1/i for each hit, where i is the position
    of the movie in the recommendation list, and then run evaluate() function.

    :param test_set: the information given by the file test.csv.
    :param cf: a collaborative-filtering object to evaluate.
    :param is_user_based: a boolean that tells which matrix to use.
    :return: a float represents the ARHR evaluation of the given CF.
    """
    def count_hits(recommendations, high_rated_movies):
        hits, i = 0, 0
        for m in recommendations:
            i += 1
            if m[0] in high_rated_movies:
                hits += 1 / i
        return hits
    val = evaluate(test_set, cf, is_user_based, count_hits, 4.0)
    print("ARHR: " + str(val))
    return val


def RSME(test_set, cf, is_user_based=True):
    """
    This function is my implementation of RMSE evaluator. It traverses the test-
    set and for each actual-rating, find the predicted-rating using the relevant
    matrix, and then calculate the precision according to RMSE formula.

    :param test_set: the information given by the file test.csv.
    :param cf: a collaborative-filtering object to evaluate.
    :param is_user_based: a boolean that tells which matrix to use.
    :return: a float represents the RMSE evaluation of the given CF.
    """
    matrix = cf.user_based_matrix if is_user_based else cf.item_based_metrix
    precision = 0.0
    for u, m, ar in zip(test_set['userId'], test_set['movieId'], test_set['rating']):
        i = cf.userId_to_index[u]
        j = cf.movieId_to_index[m]
        pr = matrix[i][j]
        precision += (pr - ar) * (pr - ar)
    val = sqrt(precision / len(test_set))
    print("RMSE: " + str(val))
    return val
