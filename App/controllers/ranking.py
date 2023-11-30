from App.models import Student, Ranking, Notification, competition_student
from App.database import db

def create_ranking(student_id):
    student = Student.query.filter_by(id=student_id).first()

    if not Student:
        return None
    
    newRanking = Ranking(student_id)
    try:
        db.session.add(newRanking)
        db.session.commit()
        return newRanking
    except Exception as e:
        db.session.rollback()
        return None

def get_ranking(id):
    ranking = Ranking.query.filter_by(student_id=id).first()
    return ranking.curr_ranking

def sort_rankings(ranking):
    return ranking.total_points
