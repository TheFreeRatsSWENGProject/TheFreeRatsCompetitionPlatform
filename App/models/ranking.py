from App.database import db
from App.models import state, change, no_change
#from .state import *
#from .change import *
#from .no_change import *

class Ranking(db.Model):
    __tablename__='ranking'

    id = db.Column(db.Integer, primary_key=True)
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, unique=True)
    total_points = db.Column(db.Integer, default=0)
    curr_ranking = db.Column(db.Integer, nullable=False, default=0)
    prev_ranking = db.Column(db.Integer, nullable=False, default=0)
    state = db.Column(db.PickleType)
  
    def __init__(self, student_id):
        self.student_id = student_id
        self.total_points = 0
        self.curr_ranking = 0
        self.prev_ranking = 0
        self.change_state = Change(self)
        self.no_change_state = NoChange(self)
        self.state = self.no_change_state

    def set_points(self, points):
        self.total_points = points

    def get_ranking(self):
        if self.curr_ranking == 0:
            return "Unranked"
        else:
            return self.curr_ranking
  
    def set_ranking(self, ranking):
        self.curr_ranking = ranking
  
    def set_previous_ranking(self, ranking):
        self.prev_ranking = ranking
  
    def update_state(self):
        self.state = self.state.update_state()

    def notify(self):
        return self.state.notify()
  
    def get_json(self):
        return {
            'total points': self.total_points,
            'rank' : self.get_ranking()
        }

    def toDict(self):
        return {
            'total points': self.total_points,
            'rank' : self.get_ranking()
        }