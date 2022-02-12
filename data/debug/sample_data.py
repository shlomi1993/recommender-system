import sys, random

def write_to_file(fname, data, title):
    with open(fname, "w") as file:
        file.write(str(title) + "\n")
        for d in data:
            file.write(str(d) + "\n")

def sample_data():

    print("creating \"movies_subset_DEBUG.csv\" file...")
    with open("movies_subset.csv", "r") as file:
        movies = file.read().split("\n")
        title = movies[0]
        movies = [movies[i] for i in range(1, len(movies))]
        indexes = random.sample(range(len(movies)), 20)
        movies = [movies[i] for i in indexes]
        movie_ids = [movies[i].split(",")[1] for i in range(20)]
        write_to_file("movies_subset_DEBUG.csv", movies, title)
    
    print("creating \"ratings_DEBUG.csv\" file...")
    with open("ratings.csv", "r") as file:
        ratings = file.read().split("\n")
        title = ratings[0]
        ratings = [ratings[i] for i in range(1, len(ratings))]
        indexes = []
        for i in range(len(ratings)):
            mid = ratings[i].split(",")[1]
            if mid in movie_ids and mid not in indexes:
                indexes.append(i)
        ratings = [ratings[i] for i in indexes]
        write_to_file("ratings_DEBUG.csv", ratings, title)
    
    print("creating \"test_DEBUG.csv\" file...")
    with open("test.csv", "r") as file:
        tests = file.read().split("\n")
        title = tests[0]
        tests = [tests[i] for i in range(1, len(tests))]
        indexes = []
        for i in range(len(tests)):
            mid = ratings[i].split(",")[1]
            if mid in movie_ids and mid not in indexes:
                indexes.append(i)
        tests = [tests[i] for i in indexes]
        write_to_file("test_DEBUG.csv", tests, title)
        
    print("Done.")
       
       
sample_data()
