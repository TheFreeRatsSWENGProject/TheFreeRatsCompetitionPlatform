from App.database import db
from .student_team import StudentTeam
from App.models.observer import Subject
from App.models.competition import Competition

class Team(db.Model, Subject):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', secondary='student_team', overlaps='teams', lazy=True)
    competitions = db.relationship('Competition', secondary='competition_team', overlaps='teams', lazy=True)

    def __init__(self, name):
        super().__init__()
        Subject.__init__(self)  # Initialize the Subject part of the Team
        self.name = name
        self.students = []

    def add_student(self, stud):
        from App.models.student import Student  # Local import to avoid circular import

        for s in self.students:
            if s.username == stud.username:
                print(f'{stud.username} is already a member of {self.name}')
                return None

        # Ensure the team is committed to the database to get a valid team_id
        if self.id is None:
            db.session.add(self)
            db.session.commit()

        stud_team = StudentTeam(student_id=stud.id, team_id=self.id)
        db.session.add(stud_team)
        db.session.commit()

        try:
            self.students.append(stud)
            stud.teams.append(self)
            db.session.commit()

            # Attach the student as an observer
            self.attach(stud)

            # Notify the student that they have been added to the team
            self.notify(event="StudentAddedToTeam", data={"team": self.name})

            # Detach the student after notification
            self.detach(stud)

            #print(f'{stud.username} was added to {self.name}!')
            return stud_team
        except Exception as e:
            db.session.rollback()
            print(f"Something went wrong adding student to team: {e}")
            return None

    def get_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "students" : [student.username for student in self.students]
        }
    
    def to_Dict(self):
        return {
            "TeamID": self.id,
            "TeamName": self.name,
            "Students": [student.username for student in self.students]
        }

    # def update(self, event, data=None):
    #     from App.models.competition import Competition  # Local import to avoid circular import

    #     if event == "TeamAdded":
    #         competition = Competition.query.filter_by(name=data['competition']).first()
    #         if competition:
    #             self.competitions.append(competition)
    #             print(f"Team Notification: {self.name}, you have been added to the competition '{data['competition']}'!")
    #         else:
    #             print(f"Competition '{data['competition']}' not found!")
    #     else:
    #         print(f"Unknown event '{event}' occurred in competition '{data.get('competition', 'unknown')}'!")
    
    def __repr__(self):
        return f'{self.name}'