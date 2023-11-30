from App.database import db
from App.models import User

class Host(User):
    __tablename__='host'
    
    id = db.Column(db.Integer, primary_key=True)
    competitions = db.relationship('Competition', secondary="competition_host", overlaps='hosts', lazy=True)
    
    def __init__(self, username, password, host_id):
        super().__init__(username, password)
        self.host_id = host_id
  
    def det_json(self):
      return {
         "id": self.id,
         "username": self.username,
         "host id": self.host_id
      }

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "host id": self.host_id
        }

    def __repr__(self):
        return f'<Host {self.id} : {self.username}>'
    