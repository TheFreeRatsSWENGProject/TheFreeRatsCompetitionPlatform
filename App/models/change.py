from App.models import state
from .state import *
from .notification import *

class Change(State):
    __tablename__='change'
  
    def notify(self, student_id, curr_ranking, prev_ranking):
        if prev_ranking == 0:
            message = f'Ranking changed from Unranked to {curr_ranking}'
        else:
            message = f'Ranking changed from {prev_ranking} to {curr_ranking}'
        notification = Notification(student_id, message)
        return notification