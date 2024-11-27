from App.database import db
from datetime import datetime
from .competition_moderator import CompetitionModerator
from .competition_team import CompetitionTeam
from App.models.observer import Subject
from App.models.notification import Notification

class Competition(db.Model, Subject):
    __tablename__ = 'competition'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    confirm = db.Column(db.Boolean, default=False)
    moderators = db.relationship('Moderator', secondary='competition_moderator', overlaps='competitions', lazy=True)
    teams = db.relationship('Team', secondary='competition_team', overlaps='competitions', lazy=True)

    def __init__(self, name, date, location, level, max_score):
        super().__init__()
        self.name = name
        self.date = date
        self.location = location
        self.level = level
        self.max_score = max_score
        self.confirm = False

    def add_mod(self, mod):
        for m in self.moderators:
            if m.id == mod.id:
                print(f'{mod.username} already added to {self.name}!')
                return None
        
        comp_mod = CompetitionModerator(comp_id=self.id, mod_id=mod.id)
        try:
            self.moderators.append(mod)
            mod.competitions.append(self)
            db.session.commit()

            # Notify observers about the moderator addition
            self.notify(event="ModeratorAdded", data={"moderator": mod.username, "competition": self.name})
            print(f'{mod.username} was added to {self.name}!')
            return comp_mod
        except Exception as e:
            db.session.rollback()
            print("Something went wrong adding mod to comp!")
            return None

    def add_team(self, team):
        for t in self.teams:
            if t.id == team.id:
                print(f'{team.name} already added to {self.name}!')
                return None
        
        comp_team = CompetitionTeam(comp_id=self.id, team_id=team.id)
        try:
            self.teams.append(team)
            team.competitions.append(self)
            db.session.commit()

            # Notify observers about the team addition
            self.notify(event="TeamAdded", data={"team": team.name, "competition": self.name})
            print(f'{team.name} was added to {self.name}!')
            return comp_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong adding team to comp!")
            return None

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%d-%m-%Y"),
            "location": self.location,
            "level": self.level,
            "max_score": self.max_score,
            "moderators": [mod.username for mod in self.moderators],
            "teams": [team.name for team in self.teams]
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Location": self.location,
            "Level": self.level,
            "Max Score": self.max_score,
            "Moderators": [mod.username for mod in self.moderators],
            "Teams": [team.name for team in self.teams]
        }

    @staticmethod
    def get_total_competitions():
        try:
            total = db.session.query(Competition).count()
            return total
        except Exception as e:
            print(f"Error fetching total competitions: {e}")
            return 0  # Default to 0 if there's an error
    
    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'
