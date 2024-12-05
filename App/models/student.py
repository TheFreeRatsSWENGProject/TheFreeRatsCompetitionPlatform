from App.database import db
from App.models import User
from App.models.observer import Observer
from App.models.notification import Notification

class Student(User, Observer):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='teams', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.prev_rank = 0
        self.teams = []
        self.notifications = []

    def add_notification(self, notification):
        if notification:
            try:
                self.notifications.append(notification)
                db.session.commit()
                return notification
            except Exception as e:
                db.session.rollback()
                return None
        return None

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count": self.comp_count,
            "curr_rank": self.curr_rank
        }

    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions": self.comp_count,
            "Rank": self.curr_rank
        }

    def update(self, event, data=None):
        if event == "StudentAddedToTeam":
            from App.models.team import Team
            team = Team.query.filter_by(name=data['team']).first()
            if team:
                self.teams.append(team)
                print(f"StudentNotification: {self.username}, you have been added to the team '{data['team']}'!")
            else:
                print(f"Team '{data['team']}' not found!")
        elif event == "RankUpdated":
            new_rank = data['curr']

            if self.prev_rank == 0:
                message = f'RANK : {new_rank}. Congratulations on your first rank!'
            elif self.curr_rank == new_rank:
                message = f'RANK : {self.curr_rank}. Well done! You retained your rank.'
            elif self.curr_rank < new_rank:
                message = f'RANK : {new_rank}. Congratulations! Your rank has went up.'
            else:
                message = f'RANK : {new_rank}. Oh no! Your rank has went down.'

            # student.prev_rank = student.curr_rank
            # ranking = Ranking(student.id, student.curr_rank, competition.date)
            # notification = Notification(student.id, message)
            # student.notifications.append(notification)


            if self.curr_rank != new_rank:
                self.prev_rank = self.curr_rank
                self.curr_rank = new_rank
                notification = Notification(self.id, message)
                self.notifications.append(notification)
                db.session.add(notification)
                db.session.commit()
                for notifation in self.notifications:
                    print(notifation.to_dict())
                # print("New rank is: ", new_rank)
                #print("Inside notification:" + str(self.to_Dict()))
                #print(f"StudentNotification: {self.username}, your rank has been updated to '{new_rank}'!")

                
        else:
            print(f"Unknown event '{event}' occurred in team '{data.get('team', 'unknown')}'!")

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'