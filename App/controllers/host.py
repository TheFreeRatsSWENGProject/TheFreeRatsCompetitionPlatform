from App.controllers.ranking import update_rankings
from App.models import Host, Competition, Student, Ranking
from App.models.competition_student import *
from App.database import db
from App.controllers import Ranking

def create_host(username, password, host_id):
    host = get_host_by_username(username)
    if host:
        print(f'{username} already exists!')
        return None

    newHost = Host(username=username, password=password, host_id=host_id)
    try:
        db.session.add(newHost)
        db.session.commit()
        print(f'New Host: {username} created!')
        return newHost
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_host_by_username(username):
    return Host.query.filter_by(username=username).first()

def get_host(id):
    return Host.query.get(id)

def get_all_hosts():
    return Host.query.all()

def get_all_hosts_json():
    hosts = Host.query.all()
    if not hosts:
        return []
    hosts_json = [host.get_json() for host in hosts]
    return hosts_json

def update_host(id, username):
    host = get_host(id)
    if host:
        host.username = username
        try:
            db.session.add(host)
            db.session.commit()
            print("Username was updated!")
            return host
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def join_comp(username, comp_name):
    host = get_host_by_username(username)
    comp = Competition.query.filter_by(name=comp_name).first()
    if not comp:
        print(f'{comp_name} does not exist!')
        return None
    
    if host:
        return comp.add_host(host)
    else:
        print("Invalid username!")
        return None

def isHost(host_id, comp_id):
    competition = Competition.query.filter_by(id=comp_id).first()

    for member in competition.hosts:
        if member.id == host_id:
            return True
    return False

def add_results(host_username, student_username, competition_name, score):
    comp = Competition.query.filter_by(name=competition_name).first()
    host = get_host_by_username(host_username)
  
    if not host:
        print(f'{host_username} is not a host')
        return None
  
    if not comp:
        print(f'{competition_name} is not a valid competition')
        return None
    
    if isHost(host.id, comp.id):
        student = Student.query.filter_by(username=student_username).first()
        
        if not student:
            print(f'{student_username} is not a valid username')
            return None

        for participant in comp.participants:
            if participant.username == student.username:
                participation = CompetitionStudent.query.filter_by(student_id=student.id, comp_id=comp.id).first()
                ranking = Ranking.query.filter_by(student_id=student.id).first()
                new_total_score = ranking.total_points + int(score) - participation.points_earned
                participation.update_points(score)
                db.session.add(participation)
                db.session.commit()
                ranking.set_points(new_total_score)
                db.session.add(ranking)
                db.session.commit()
                update_rankings()

                print("Score added!")
                return True

        print(f'{student_username} did not participate in {competition_name}')
        return False
    else:
        print(f'{host_username} does not have access to add results for {competition_name}')
        return False