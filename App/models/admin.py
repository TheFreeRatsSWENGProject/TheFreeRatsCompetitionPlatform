from App.database import db
from App.models import User

class Admin(User):
    __tablename__ = 'admin'

    competitions = db.relationship('Competition', secondary='competition_admin', overlaps='admins', lazy=True)

    def __init__(self, username, password, staff_id):
        super().__init__(username, password)
        self.competitions = []

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
        }

    def toDict(self):
        return{
            'ID': self.id,
            'Username': self.username,
        }