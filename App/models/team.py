from App.database import db

class Team(db.Model):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', secondary='student_team', overlaps='teams', lazy=True)
    competitions = db.relationship('Competition', secondary='competition_team', overlaps='teams', lazy=True)

    def __init__(self, name):
        self.name = name
        self.students = []

    def get_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "students" : [student.username for student in self.students]
        }
    
    def to_Dict(self):
        return {
            "ID" : self.id,
            "Name" : self.name,
            "Students" : [student.username for student in self.student]
        }