from App.database import db#from App.controllers.ranking import create_ranking
from App.models import Student, Competition, Notification#, Ranking, competition_student

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
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

"""
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
"""
def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        """
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
        """
        return student.get_json()

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_Dict() for notification in student.notifications]}
"""
def get_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return student.notifications
"""

def update_rankings():
    students = get_all_students()

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score
    curr_rank = 1
        
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        #team = Team.query.filter_by(id=comp_team.team_id).first()
        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1
        
            student.curr_rank = curr_rank
            if student.prev_rank == 0:
                message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
            elif student.curr_rank == student.prev_rank:
                message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
            elif student.curr_rank < student.prev_rank:
                message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
            else:
                message = f'RANK : {student.curr_rank}. Oh on! Your rank has went down.'
            student.prev_rank = student.curr_rank
            notification = Notification(student.id, message)
            student.notifications.append(notification)

            try:
                db.session.add(student)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return leaderboard

def display_rankings():
    students = get_all_students()

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score
    curr_rank = 1
        
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

    print("Rank\tStudent\tRating Score")

    for position in leaderboard:
        print(f'{position["placement"]}\t{position["student"]}\t{position["rating score"]}')