from App.database import db
from datetime import datetime

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    admins = db.relationship('Admin', secondary="competition_admin", overlaps='competitions', lazy=True)
    teams = db.relationship('Team', secondary="competition_team", overlaps='competitions', lazy=True)

    def __init__(self, name, date, location):
        self.name = name
        self.date = date
        self.location = location
        self.admins = []
        self.teams = []
    
    def add_host(self, host):
        for h in self.hosts:
            if h.id == host.id:
                print("Host already added!")
                return None
        
        comp_host = CompetitionHost(comp_id=self.id, host_id=host.host_id)
        try:
            self.hosts.append(host)
            host.competitions.append(self)
            db.session.commit()
            print(f'{host.username} was added to {self.name}!')
            return comp_host
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None



    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "admins": [admin.username for admin in self.admins],
            "teams": [team.name for team in self.teams]
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Location": self.location,
            "Admins": [admin.username for admin in self.admins],
            "Teams": [team.name for team in self.teams]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'