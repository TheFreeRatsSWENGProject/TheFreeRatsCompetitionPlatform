from App.database import db
from App.models import User
from App.models.observer import Observer
from App.models.competition import Competition

class Moderator(User, Observer):
    __tablename__ = 'moderator'

    competitions = db.relationship('Competition', secondary='competition_moderator', overlaps='moderators', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.competitions = []

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'competitions': [comp.name for comp in self.competitions]
        }

    def toDict(self):
        return {
            'ID': self.id,
            'Username': self.username,
            'Competitions': [comp.name for comp in self.competitions]
        }

    def update(self, event, data=None):
        if event == "ModeratorAdded":
            competition = Competition.query.filter_by(name=data['competition']).first()
            if competition:
                self.competitions.append(competition)
                print(f"Moderator Notification: {self.username}, you have been added to the competition '{data['competition']}'!")
            else:
                print(f"Competition '{data['competition']}' not found!")
        else:
            print(f"Unknown event '{event}' occurred in competition '{data.get('competition', 'unknown')}'!")

    def __repr__(self):
        return f'{self.username}'
