from App.database import db
from App.models import User

class Admin(User):
    __tablename__ = 'admin'

    staff_id = db.Column(db.Integer, unique=True)

    def __init__(self, username, password, staff_id):
        super().__init__(username, password)
        self.staff_id = staff_id

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username
        }
