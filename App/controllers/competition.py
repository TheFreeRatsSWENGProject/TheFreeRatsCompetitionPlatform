from App.models import Competition, Student, Admin, competition_student
from App.database import db

def create_competition(name, staff_id):
    comp = get_competition_by_name(name)
    if comp:
        print(f'{name} already exists!')
        return None
    
    admin = Admin.query.filter_by(staff_id=staff_id).first()
    if admin:
        newComp = Competition(name=name)
        try:
            db.session.add(newComp)
            db.session.commit()
            print(f'New Competition: {name} created!')
            return newComp
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None
    else:
        print("Invalid credentials!")

def get_competition_by_name(name):
    return Competition.query.filter_by(name=name).first()

def get_competition(id):
    return Competition.query.get(id)

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()

    if not competitions:
        return []
    else:
        return [comp.get_json() for comp in competitions]

#still needs adjusting (add_results function)
"""def add_results(user_id, comp_id, rank):
    Comp = Competition.query.get(comp_id)
    user = User.query.get(user_id)
          
    if user and Comp:
        compParticipant = UserCompetition(user_id = user.id, comp_id = Comp.id, rank=rank)

        try:
            db.session.add(compParticipant)
            db.session.commit 
            print("successfully added user to comp")
            return True
        except Exception as e:
            db.session.rollback()
            print("error adding to comp")
            return False
        return False

def get_competition_students(comp_id):
    comp = get_competition(comp_id)

    if comp:
        return [Student.query.get(student_id) for student in comp.participants]
    return []"""