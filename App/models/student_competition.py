from App.database import db

class StudentCompetition(db.Model):
    __tablename__ = 'student_competition'
    
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    points_earned = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, student_id, competition_id):
      self.student_id = student_id
      self.comp_id = competition_id

    def update_points(self, points_earned):
      self.points_earned = points_earned
    
    def toDict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'competition_id': self.comp_id,
            'points_earned': self.points_earned
        } 

    def get_json(self):
      return {
          'id': self.id,
          'student_id': self.student_id,
          'competition_id': self.comp_id,
          'points_earned': self.points_earned
      }
