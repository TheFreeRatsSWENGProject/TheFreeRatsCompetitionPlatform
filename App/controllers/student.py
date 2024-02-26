#from App.controllers.ranking import create_ranking
from App.models import Student#, Competition, Ranking, competition_student
from App.database import db

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
        #create_ranking(newStudent.id)
        print(f'New Student: {username} created!')
        return newStudent
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def register_student(username, competition_name):
  student = get_student_by_username(username)
  if student:
    competition = Competition.query.filter_by(name=competition_name).first()
    if competition:
      return student.participate_in_competition(competition)
    else:
      print(f'{competition_name} was not found')
      return None
  else:
    print(f'{username} was not found')
    return None

def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        ranking = Ranking.query.filter_by(student_id=student.id).first()
        if ranking:
            profile_info = {
                "profile": student.get_json(),
                "ranking": ranking.get_json(),
                "participated_competitions": [comp.name for comp in student.competitions]
            }
        else:
            profile_info = {
                "profile": student.get_json(),
                "participated_competitions": [comp.name for comp in student.competitions]
            }
        return profile_info

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.get_json() for notification in student.notifications]}

def get_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return student.notifications