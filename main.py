import random
import time
from email_test import *


def get_random_movies(n, movies):
    index_list = []
    hIndex = hash(time.ctime())
    for i in range(n):
        hIndex = hash(int(hIndex) + n)
        index_list.append(hIndex % len(movies))
    
    if n == 3:
        message = f"Here are the options:\n1. {movies[index_list[0]]}\n2. {movies[index_list[1]]}\n3. {movies[index_list[2]]}"
        instructions = "\n\nText back the number of the movie you vote for (1-3)."
        return message+instructions, [movies[index_list[0]], movies[index_list[1]], movies[index_list[2]]]
    else:
        message = f"You are watching: {movies[index_list[0]]} (A tie or 4 won).", movies[index_list[0]]


    return message

def read_list_of_movies():
    with open("movies.txt", "r") as f:
        data = f.read()
        movies = data.split("\n")
        
        #Remove final line
        movies.pop(len(movies)-1)

    return movies

def write_list_of_movies(movies):
    # Write current list of movies to file:
    with open("movies.txt", "w") as f:
        for i in movies:
            f.write(i+"\n")

if __name__ == "__main__":
    print("Running...")
    acceptableTimes = ["09:00", "09:01"]
    while(1):
        time_check = (time.ctime()[11:16] == "09:00") or (time.ctime()[11:16] in acceptableTimes)

        if time_check and check_for_movie_approval():
            #Read list of movies to a list:
            movies = read_list_of_movies()
            print("List generated...")
            
            movString, options = get_random_movies(3, movies)

            print(movString)

            #Send email of movies
            send_email("", movString)
            time.sleep(2)
            send_email("", "If you do not vote today by 1:00 PM then your won't have a say in this movie.  You can also vote 4 (or hope for a tie) and the movie will be random.  Last vote counts.")
            print("Emails sent...")

            #Wait till 1:00 PM (ish).  Should be 4 hours
            time.sleep(60*60*4)

            #Read votes
            winning_vote = read_votes()
            print("Votes read...")

            if winning_vote == 4:
                finalMovString, winner = get_random_movies(1, movies)
            else:
                finalMovString = options[winning_vote-1] + " won."
                winner = options[winning_vote-1]
            
            #Send result
            send_email("", finalMovString)
            print("Final email sent...")

            movies.remove(winner)
            write_list_of_movies(movies)
    
    exit(0)
