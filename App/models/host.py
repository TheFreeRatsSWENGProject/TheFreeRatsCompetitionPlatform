from App.database import db
from App.models import User

class Host(User):
    __tablename__='host'
    
    host_id = db.Column(db.Integer, unique=True)
    competitions = db.relationship('Competition', secondary="competition_host", overlaps='hosts', lazy=True)
    
    def __init__(self, username, password, host_id):
        super().__init__(username, password)
        self.host_id = host_id
  
    def get_json(self):
      return {
         "id": self.id,
         "username": self.username,
         "role": 'Host',
         "host id": self.host_id,
         "competitions": [comp.get_json() for comp in self.competitions]
      }

    def toDict(self):
      return {
          "id": self.id,
          "username": self.username,
          "role": 'Host',
          "host id": self.host_id,
          "competitions": [comp.toDict() for comp in self.competitions]
        }

    def __repr__(self):
        return f'<Host {self.id} : {self.username}>'
    