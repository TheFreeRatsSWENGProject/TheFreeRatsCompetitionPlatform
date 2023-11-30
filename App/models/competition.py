from datetime import datetime
from App.database import db

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)

    hosts = db.relationship('Host', secondary="competition_host", overlaps='competitions', lazy=True)
    participants = db.relationship('Student', secondary="student_competition", overlaps='competitions', lazy=True)

    def __init__(self, name, location):
        self.name = name
        self.location = location
    
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'location': self.location,
            'hosts' : [host.username for host in self.hosts],
            'participants': [student.username for student in self.participants]
        }

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "hosts": [host.toDict() for host in self.hosts],
            "participants": [participant.toDict() for participant in self.participants]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'
