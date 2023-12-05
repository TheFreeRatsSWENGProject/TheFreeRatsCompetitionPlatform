from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import *


comp_views = Blueprint('comp_views', __name__, template_folder='../templates')


##return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitons():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200) 

##add new competition to the db
@comp_views.route('/competitions', methods=['POST'])
def add_new_comp():
    data = request.json
    response = create_competition(data['name'], data['location'])
    if response:
        return (jsonify({'message': f"competition created"}), 201)
    return (jsonify({'error': f"error creating competition"}),500)


@comp_views.route('/competitions/user', methods=['POST'])
def add_comp_user():
    data = request.json
    response = add_new_user()
    if response: 
        return (jsonify({'message': f"user added to competition"}),201)
    return (jsonify({'error': f"error adding user to competition"}),500)

@comp_views.route('/competitions/<int:id>', methods=['GET'])
def get_competition(id):
    competition = get_competition(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404 
    return (jsonify(competition.toDict()),200)

@comp_views.route('/competitions/results', methods=['POST'])
def add_comp_results():
    data = request.json
    response = add_results(data['Host_username'],data['Student_username'], data['comp_name'], data['score'])
    if response:
        return (jsonify({'message': f"results added successfully"}),201)
    return (jsonify({'error': f"error adding results"}),500)

@comp_views.route('/rankings/<int:id>', methods =['GET'])
def get_rankings(id):
    ranks = get_ranking(id)
    return (jsonify(ranks),200)




