from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

#two API endpoints/routes:
#first API endpoint/route - add movie
@main.route('/add_movie', methods=['POST'])
def add_movie():
    return 'Done', 201 #status 201 means something was created successfully 

#second endpoint - display movie
@main.route('/movies')
def movies():

    movies=[] #empty array/list
    
    #convert array/list to JSON data
    return jsonify({'movies' : movies})