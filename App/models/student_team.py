from App.database import db

class StudentTeam(db.Model):
    __tablename__ = 'student_team'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __init__(self, student_id, team_id):
        self.student_id = student_id
        self.team_id = team_id
    
    def get_json(self):
        return {
            "id" : self.id,
            "student_id" : self.student_id,
            "team_id" : self.team_id
        }
    
    def to_Dict(self):
      return {
            "ID" : self.id,
            "Student ID" : self.student_id,
            "Team ID" : self.team_id
      }