from App.database import db
from App.models import User, student_competition, competition

class Student(User):
    __tablename__ = 'student'

    competitions = db.relationship('Competition', secondary="student_competition", overlaps='participants', lazy=True)
    ranking = db.relationship('Ranking', uselist=False, backref='student', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
    
    def participate_in_competition(self, competition):
      registered = False
      for comp in self.competitions:
        if (comp.id == competition.id):
          registered = True

      if isinstance(self, Student) and not registered:
          participation = Participation(student_id=self.id, competition_id=competition.id)
          try:
            self.competitions.append(competition)
            competition.participants.append(self)
            db.session.commit()
          except Exception as e:
            db.session.rollback()
            return None
          else:
            print(f'{self.username} was registered for {competition.name}')
            return participation
      else:
          print(f'{self.username} is already registered for {competition.name}')
          return None

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": 'Student'
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'
