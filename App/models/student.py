from App.database import db
from App.models import User#, competition_student, competition
from .competition_student import *

class Student(User):
    __tablename__ = 'student'

    competitions = db.relationship('Competition', secondary="competition_student", overlaps='participants', lazy=True)
    ranking = db.relationship('Ranking', uselist=False, backref='student', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
    
    def participate_in_competition(self, competition):
      for comp in self.competitions:
        if (comp.id == competition.id):
          print(f'{self.username} is already registered for {competition.name}!')
          return None

      comp_student = CompetitionStudent(student_id=self.id, competition_id=competition.id)
      try:
        self.competitions.append(competition)
        competition.participants.append(self)
        db.session.commit()
        print(f'{self.username} was registered for {competition.name}')
        return comp_student
      except Exception as e:
        db.session.rollback()
        print("Something went wrong!")
        return None

    def add_notification(self, notification):
        if notification:
          try:
            self.notifications.append(notification)
            db.session.commit()
            return notification
          except Exception as e:
            db.session.rollback()
            return None
        return None

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": 'Student'
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'