from App.database import db
from App.models import host
from .competition_host import *

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    #date = db.Column(db.DateTime, default= datetime.utcnow)
    #location = db.Column(db.String(120), nullable=False)

    #host_id = db.Column(db.Integer, nullable=False)
    hosts = db.relationship('Host', secondary="competition_host", overlaps='competitions', lazy=True)
    participants = db.relationship('Student', secondary="competition_student", overlaps='competitions', lazy=True)

    def __init__(self, name):
        self.name = name
        #self.location = location
    
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
            'id': self.id,
            'name': self.name,
            #'date': self.date,
            #'location': self.location,
            'hosts' : [host.username for host in self.hosts],
            #'host_id': self.host_id,
            'participants': [student.username for student in self.participants]
        }

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            #"date": self.date,
            #"location": self.location,
            "hosts": [host.username for host in self.hosts],
            #"host_id": self.host_id,
            "participants": [participant.toDict() for participant in self.participants]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'