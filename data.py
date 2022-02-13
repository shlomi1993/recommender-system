# Shlomi Ben-Shushan


import matplotlib.pyplot as plt


def watch_data_info(data):
    """
    This function prints useful information about the given data.

    :param data: a tuple of data from ratings.csv and movies_subset.csv files.
    :return: None. Prints information instead.
    """
    for d in data:
        print(d.head())
        print(d.info())
        print(d.describe(include='all').transpose())


def print_data(data):
    """
    This function prints the required information to answer the questions in the
    first part of the exercise.

    :param data: a tuple of data from ratings.csv and movies_subset.csv files.
    :return: None. Prints information instead.
    """
    ratings = data[0]

    # Get initial information.
    n_ratings = len(ratings)
    n_movies = len(ratings['movieId'].unique())
    n_users = len(ratings['userId'].unique())

    # Count ratings for each user and movie in the dataset.
    u_counters, m_counters = {}, {}
    for u, m in zip(ratings['userId'], ratings['movieId']):
        if u in u_counters.keys():
            u_counters[u] += 1
        else:
            u_counters[u] = 1
        if m in m_counters.keys():
            m_counters[m] += 1
        else:
            m_counters[m] = 1

    # Calculate the keys of the minimum and maximum values in each dictionary.
    u_min_k = min(m_counters.keys(), key=lambda k: m_counters[k])
    u_max_k = max(m_counters.keys(), key=lambda k: m_counters[k])
    m_min_k = min(u_counters.keys(), key=lambda k: u_counters[k])
    m_max_k = max(u_counters.keys(), key=lambda k: u_counters[k])

    # Print the required information to answer questions 1, 2 and 3.
    print(f"The number of unique users is {n_users}.")
    print(f"The number of unique movies is {n_movies}.")
    print(f"The number of ratings is {n_ratings}.")
    print(f"The minimum number of ratings that given to a movie is {m_counters[u_min_k]}.")
    print(f"The maximum number of ratings that given to a movie is {m_counters[u_max_k]}.")
    print(f"The minimum number of ratings that a user gave is {u_counters[m_min_k]}.")
    print(f"The maximum number of ratings that a user gave is {u_counters[m_max_k]}.")


def plot_data(data, plot=True):
    """
    This function plots the rating distribution and save it to a file.

    :param data: a tuple of data from ratings.csv and movies_subset.csv files.
    :param plot: a boolean that tells if to plot the graph or not.
    :return: None. Create plot file and show it if needed instead.
    """
    ratings = data[0]['rating'].sort_values(ascending=True)

    # Count votes for each rating.
    counters = {}
    for x in ratings:
        xs = str(x)
        if xs in counters.keys():
            counters[xs] += 1
        else:
            counters[xs] = 0

    # Create a plot and save it as an image in a folder named "plot".
    rates = list(counters.keys())
    count = list(counters.values())
    plt.figure()
    plt.bar(rates, count)
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    try:
        plt.savefig("plot/Rating Distribution.png")
    except FileNotFoundError:
        print("Error: plot folder could not be found so the figure was not saved.")

    # Show plot if required.
    if plot:
        plt.show()
