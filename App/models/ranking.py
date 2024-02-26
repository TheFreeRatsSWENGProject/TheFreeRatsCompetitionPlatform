from App.database import db

class Ranking(db.Model):
    __tablename__='ranking'

    id = db.Column(db.Integer, primary_key=True)
    student_id =  db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False, unique=True)
    total_points = db.Column(db.Integer, default=0)
    curr_ranking = db.Column(db.Integer, nullable=False, default=0)
    prev_ranking = db.Column(db.Integer, nullable=False, default=0)
  
    def __init__(self, student_id):
        self.student_id = student_id
        self.total_points = 0
        self.curr_ranking = 0
        self.prev_ranking = 0
    """
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
        self.change_state = Change()
        self.no_change_state = NoChange()
        if self.curr_ranking != self.prev_ranking:
            if self.curr_ranking <= 20 or (self.prev_ranking <= 20 and self.prev_ranking != 0):
                self.state = self.change_state
            else:
                self.prev_ranking = self.curr_ranking
                self.update_state()
                db.session.add(self)
                db.session.commit()
        else:
            self.state = self.no_change_state

    def notify(self):
        notification = self.state.notify(self.student_id, self.curr_ranking, self.prev_ranking)
        if notification:
            self.prev_ranking = self.curr_ranking
            self.update_state()
            db.session.add(self)
            db.session.commit()
        return notification
    """
    def get_json(self):
        return {
            'rank' : self.get_ranking(),
            'total points': self.total_points
        }

    def toDict(self):
        return {
            'rank' : self.get_ranking(),
            'total points': self.total_points
        }