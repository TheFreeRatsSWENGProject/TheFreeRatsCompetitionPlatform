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
    return render_template('competitions.html', competitions=get_all_competitions())
    #return (jsonify(competitions),200) 

##add new competition to the db
@comp_views.route('/competitions', methods=['POST'])
def add_new_comp():
    data = request.json
    response = create_competition(data['name'], data['date'], data['location'], data['level'], data['max score'])
    if response:
        return (jsonify({'message': "Competition created!"}), 201)
    return (jsonify({'error': "Error creating competition"}),500)

#create new comp
@comp_views.route('/createcompetition', methods=['POST'])
def create_comp():
    data = request.form
    response = create_competition('mod1', data['name'], data['date'], data['location'], data['level'], data['max score'])
    if response:
        return (jsonify({'message': "Competition created!"}), 201)
    return (jsonify({'error': "Error creating competition"}),500)

#page to create new comp
@comp_views.route('/createcompetition', methods=['GET'])
def create_comp_page():
    return render_template('competition_creation.html', students=get_all_students(), competitions=get_all_competitions())

"""
@comp_views.route('/competitions/moderator', methods=['POST'])
def add_comp_moderator():
    data = request.json
    response = add_mod()
    if response: 
        return (jsonify({'message': f"user added to competition"}),201)
    return (jsonify({'error': f"error adding user to competition"}),500)
"""
@comp_views.route('/competitions/<int:id>', methods=['GET'])
def competition_details(id):
    competition = get_competition(id)
    if not competition:
        return render_template('404.html')
    
    #team = get_all_teams()

    #teams = get_participants(competition_name)
    return render_template('competition_details.html', competition=competition)#, team=team)

    #teams = get_participants(competition_name)
    #return render_template('Competition_Details.html', competition=competition)

""" @index_views.route('/competition/<string:name>', methods=['GET'])
def competition_details(name):
    competition = get_competition_by_name(name)
    if not competition:
        return render_template('404.html')

    #teams = get_participants(competition_name)
    return render_template('Competition_Details.html', competition=competition) """

@comp_views.route('/competitions/results', methods=['POST'])
def add_comp_results():
    data = request.json
    response = add_results(data['mod_name'], data['comp_name'], data['team_name'], data['score'])
    if response:
        return (jsonify({'message': "Results added successfully!"}),201)
    return (jsonify({'error': "Error adding results!"}),500)

@comp_views.route('/competitions/results/<int:id>', methods =['GET'])
def get_results(id):
    competition = get_competition(id)
    leaderboard = display_competition_results(competition.name)
    if not leaderboard:
        return jsonify({'error': 'Leaderboard not found!'}), 404 
    return (jsonify(leaderboard),200)