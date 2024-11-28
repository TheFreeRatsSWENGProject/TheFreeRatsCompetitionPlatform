from App.database import db
from .student_team import *
from App.models.observer import Observer
class Team(db.Model, Observer):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', secondary='student_team', overlaps='teams', lazy=True)
    competitions = db.relationship('Competition', secondary='competition_team', overlaps='teams', lazy=True)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.students = []

    def add_student(self, stud):
        for s in self.students:
            if s.username == stud.username:
                print(f'{stud.username} is already a member of {self.name}')
                return None
        
        stud_team = StudentTeam(student_id=stud.id, team_id=self.id)
        try:
            self.students.append(stud)
            stud.teams.append(self)
            db.session.commit()
            print(f'{stud.username} was added to {self.name}!')
            return stud_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong adding student to team!")
            return None

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

    def update(self, event, data=None):
        if event == "TeamAdded":
            print(f"Team Notification: {self.name}, you have been added to the competition '{data['competition']}'!")
        else:
            print(f"Unknown event '{event}' occurred.")
    
    def __repr__(self):
        return f'{self.name}'