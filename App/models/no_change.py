from App.models import state
from .state import *

class NoChange(State):
    __tablename__='no_change'

    def notify(self, student_id, curr_ranking, prev_ranking):
        return None