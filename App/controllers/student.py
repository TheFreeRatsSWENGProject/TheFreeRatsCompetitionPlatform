from App.database import db
from datetime import datetime
from App.models import Student, Competition, Notification, CompetitionTeam, Subject, Team, RankHistory

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
        #print(f'New Student: {username} created!')
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

def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        competitions = []
        
        for team in student.teams:
            team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()
            for comp_team in team_comps:
                comp = Competition.query.filter_by(id=comp_team.comp_id).first()
                competitions.append(comp.name)

        profile_info = {
            "profile" : student.get_json(),
            "competitions" : competitions
        }

        return profile_info

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_dict() for notification in student.notifications]}


def create_ranking(student_id, rank, date, score):
    ranking = RankHistory(student_id, rank, date,score)
    
    try:
        db.session.add(ranking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Error creating ranking: {e}')

def update_rankings(comp_name):
    students = get_all_students()
    competition = Competition.query.filter_by(name=comp_name).first()
    from App.models import RankingSubject
    ranking_subj = RankingSubject()
    # Sort by rating_score, comp_count, and a unique identifier (e.g., student.id)
    students.sort(key=lambda x: (x.rating_score, x.comp_count, x.id), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score if students else 0
    curr_rank = 1


    for student in students:
        ranking_subj.attach(student)
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        ranking_subj.notify("RankUpdated", {"curr": curr_rank})
        ranking_subj.detach(student)

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score": student.rating_score})
            count += 1

            student.prev_rank = student.curr_rank

           
            try:
                db.session.add(student)
                # db.session.add(rank_history)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f'Error updating student rank: {e}')
                
            create_ranking(student.id, student.curr_rank, competition.date,student.rating_score)
        else:
            create_ranking(student.id, 0, competition.date,student.rating_score)

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
    
    return leaderboard


def display_rank_history(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return
    
    history = RankHistory.query.filter_by(student_id=student.id).order_by(RankHistory.date.desc()).all()
    history.sort(key=lambda x: (x.id), reverse=True)

    print("Rank\tDate\t\t\t\tScore")
    for rank in history:
        print(f'{rank.rank}\t{rank.date}\t{rank.score}')

    return history


def get_rank_history_json(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return
    
    history = RankHistory.query.filter_by(student_id=student.id).order_by(RankHistory.date.desc()).all()

    if not history:
        return []
    else:
        return [rank.get_json() for rank in history]
    
