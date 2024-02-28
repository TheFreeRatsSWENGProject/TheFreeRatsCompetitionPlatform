from App.database import db
from App.models import Team, Competition

def create_team(team_name, students):
    team = Team(name=team_name)
    try:
        for s in students:
            stud = Student.query.filter_by(username=stud.username).first()
            team.add_student(stud)
        db.session.add(team)
        db.session.commit()
        print(f'New Team: {team_name} created!')
        return team
    except Exception as e:
        db.session.rollback()
        print("Something went wrong!")
        return None

def get_team_by_name(name):
    return Team.query.filter_by(name=name).first()

def get_team(id):
    return Team.query.get(id)

def get_all_teams():
    return Team.query.all()

def get_all_teams_json():
    teams = Team.query.all()

    if not teams:
        return []
    else:
        return [team.get_json() for team in teams]
    
def find_team(team_name, students):
    teams = Team.query.filter_by(name=team_name).all()

    for team in teams:
        if set(team.students) == set(students):
            return team
    
    return None