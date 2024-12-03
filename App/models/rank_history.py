from App.database import db
from datetime import datetime

class RankHistory(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False)  # Add score field

    def __init__(self, student_id, rank, date, score):
        self.student_id = student_id
        self.rank = rank
        self.date = date
        self.score = score

    def get_json(self):
        if self.rank == 0:
            return {
                "student_id": self.student_id,
                "rank": "Unranked",
                "date": self.date.strftime("%Y-%m-%d"),  # Format date
                "score": self.score
            }
        else:
            return {
                "student_id": self.student_id,
                "rank": self.rank,
                "date": self.date.strftime("%Y-%m-%d"),  # Format date
                "score": self.score
            }