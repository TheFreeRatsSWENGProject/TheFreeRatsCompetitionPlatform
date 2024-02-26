#from App.models import Student, Ranking, Notification, competition_student
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

    if ranking:
        return ranking
    else:
        return None

def sort_rankings(ranking):
    return ranking.total_points

def update_rankings():
    rankings = Ranking.query.all()
    count = 1
    if rankings:
        rankings.sort(key=sort_rankings,reverse=True)
        curr_high = rankings[0].total_points
        curr_rank = 1
        for ranking in rankings:
            if curr_high != ranking.total_points:
                curr_rank = count
                curr_high = ranking.total_points
            ranking.set_ranking(curr_rank)
            ranking.update_state()
            db.session.add(ranking)
            db.session.commit()
            notification = ranking.notify()
            if notification:
                student = Student.query.filter_by(id=ranking.student_id).first()
                student.add_notification(notification)
                db.session.add(student)
                db.session.commit()
            count += 1

def display_rankings():
    rankings = Ranking.query.all()
    if not rankings:
        print("No Rankings found!")
        return None
    else:
        leaderboard = []
        count = 1
        rankings.sort(key=sort_rankings,reverse=True)
        curr_high = rankings[0].total_points
        curr_rank = 1
        for ranking in rankings:
            if curr_high != ranking.total_points:
                curr_rank = count
                curr_high = ranking.total_points

            student = Student.query.filter_by(id=ranking.student_id).first()
            leaderboard.append({"student": student.username, "ranking":ranking.get_json()})
            count += 1
        return leaderboard