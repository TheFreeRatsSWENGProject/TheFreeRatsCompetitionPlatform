from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html', users=get_all_students(),get_ranking=get_ranking,display_rankings=display_rankings,competitions=get_all_competitions())

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_student('bob', 'bobpass')
    create_student('alice', 'alicepass')
    create_student('charlie', 'charliepass')
    create_student('david', 'davidpass')
    create_admin('admin', 'adminpass',1)
    create_host('admin2', 'adminpass2',2)
    create_host('admin3', 'adminpass3',3)
    create_competition('RunTime', 1)
    join_comp('admin2', 'RunTime')
    register_student('bob', 'RunTime')
    register_student('alice', 'RunTime')
    register_student('charlie', 'RunTime')
    register_student('david', 'RunTime')
    create_competition('RunTime2', 1)
    add_results('admin2', 'bob', "RunTime",5)
    add_results('admin2', 'alice', "RunTime",10)
    add_results('admin2', 'charlie', "RunTime",15)
    create_competition('RunTime3', 1)
    join_comp('admin3', 'RunTime3')
    register_student('bob', 'RunTime3')
    register_student('alice', 'RunTime3')
    register_student('charlie', 'RunTime3')
    add_results('admin3', 'bob', "RunTime3",5)
    add_results('admin3', 'alice', "RunTime3",10)
    add_results('admin3', 'charlie', "RunTime3",15)

    return jsonify(message='The Database has been successfully initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/healthcheck', methods=['GET'])
def health():
    return jsonify({'status':'healthy'})

#@index_views.route('/Student_Profile/<int:user_id>')
#def Student_Profile(user_id):
 #   return render_template('Student_Profile.html', user_id=user_id)



@index_views.route('/Student_Profile/<int:user_id>')
def Student_Profile(user_id):
    user =get_student(user_id)

    if not user:
        return render_template('404.html')
    competitions = Competition.query.filter(Competition.participants.any(id=user_id)).all()
    ranking = Ranking.query.filter_by(student_id=user_id).first()
    notifications= get_notifications(user.username)

    return render_template('Student_Profile.html', user=user, competitions=competitions, ranking=ranking, notifications=notifications)


@index_views.route('/competition/<string:competition_name>', methods=['GET'])
def Competition_Details(competition_name):
    competition = get_competition_by_name(competition_name)
    if not competition:
        return render_template('404.html')

    participants = get_participants(competition_name)
    return render_template('Competition_Details.html', competition=competition, participants=participants)


@index_views.route('/register_competition', methods=['POST'])
def Register_Competition():
    username = request.form.get('username')
    competition_name = request.form.get('competition_name')

    result = register_student(username, competition_name)
    if result:
        return f'Successfully registered {username} for {competition_name}'
    else:
        return 'Registration failed'


@index_views.route('/Student_Ranking/<int:user_id>')
def Student_Rankk(user_id):
    user =get_student(user_id)

    if not user:
        return render_template('404.html')
    competitions = Competition.query.filter(Competition.participants.any(id=user_id)).all()
    ranking = Ranking.query.filter_by(student_id=user_id).first()

    ranking= ranking.curr_ranking

    return jsonify(ranking) 


@index_views.route('/api/admin', methods=['POST'])
def create_adminV():
    data = request.json
    admin = create_admin(data['username'], data['password'], data['staff_id'])
    if admin:
        return jsonify({'message': f"admin {admin.username} created"})
    else:
        return jsonify({'message': f"Failed to create admin"})

