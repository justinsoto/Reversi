
from model.game import Game
from view.console_items.console_game_view import ConsoleGameView
from controller.controller import GameController
from mysql.connector import connect, Error
from getpass import getpass
from database.db_management.user_manager import UserManager
from database.db_management.games_manager import GamesManager
from database.db_management.ratings_manager import RatingsManager

connection = None # initialize connection variable to None to handle connection closure in the finally block at the bottom of file
try:
    # attempt to establish a database connection with credentials provided by the user
    connection = connect(host='localhost', user=input('Enter Username: '), password=getpass('Enter Password: '), database="Othello" )
    user_manager = UserManager(connection)
    ratings_manager = RatingsManager(connection)
    games_manager = GamesManager(connection)

    #create user
    user_manager.create_user("User11","MyPassword")
    user_id = user_manager.get_current_user().get_user_id() # could use this in the future, when we have login
    #then if create manager takes in user_id, we can use this to create ratings for the user --> rn its an auto incrementing primary key
    user_manager.create_user("User21","MyPassword2")
    user_id2 = user_manager.get_current_user().get_user_id()
    user_manager.create_user("User31","MyPassword3")
    user_id3 = user_manager.get_current_user().get_user_id()

    # create ratings for user -- rn this doesnt quite work like we want it cuz were dont have login functionality yet so we dont actually create users
    # the user_id (primary key) for the ratings table just auto increments rn
    ratings_manager.create_rating(10, 5, 3) #lets pretend this is user1 rating for now
    rating_user_id1 = ratings_manager.get_current_rating().get_user_id() #again this user_id will come from user and not be auto_increment when we have login functionality
    ratings_manager.create_rating(20, 10, 5) #lets pretend this is user2 rating for now
    rating_user_id2 = ratings_manager.get_current_rating().get_user_id()
    ratings_manager.create_rating(30, 15, 7) #lets pretend this is user3 rating for now
    rating_user_id3 = ratings_manager.get_current_rating().get_user_id()

    #update user1's top score and wins
    ratings_manager.update_top_score(int(rating_user_id1), 15)
    ratings_manager.update_wins(int(rating_user_id1), 7)

    #delete all three users and ratings
    user_manager.delete_user(user_id)
    user_manager.delete_user(user_id2)
    user_manager.delete_user(user_id3)

    ratings_manager.delete_rating(rating_user_id1)
    ratings_manager.delete_rating(rating_user_id2)
    ratings_manager.delete_rating(rating_user_id3)

except Error as err:
    # catch and print any errors that occur during connection or database operations
    print("Error:", err)

finally:
    # close the databse connection if it was successfully established
    if connection is not None:
        connection.close()
