from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'

    rating_score = db.Column(db.Integer, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    #participations = db.relationship('Competition', secondary='competition_team', overlaps='student', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.prev_rank = 0
        self.teams = []
        self.participations = []
        self.notifications = []
    
    """
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
    """

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
            "rating_score": self.rating_score,
            "comp_count" : self.comp_count,
            "curr_rank" : self.curr_rank
        }

    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions" : comp_count,
            "Rank" : self.curr_rank
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'