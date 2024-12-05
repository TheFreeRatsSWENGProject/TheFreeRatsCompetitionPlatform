from App.database import db
from App.models.observer import Observer

class Notification(db.Model, Observer):  #extend da observer
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    message = db.Column(db.String, nullable=False)

    def __init__(self, student_id, message=""):
        self.student_id = student_id
        self.message = message

    def update(self, event, data=None):
        """
        Respond to a Subject's notifications.
        This method is triggered when the Subject calls notify().
        """
        if event == "TeamAdded":
            self.message = f"New team '{data['team']}' added to competition '{data['competition']}'!"
        elif event == "ModeratorAdded":
            self.message = f"Moderator '{data['moderator']}' added to competition '{data['competition']}'!"
        else:
            self.message = f"Unknown event '{event}' occurred in competition '{data.get('competition', 'unknown')}'!"

        # Save notification in database 
        try:
            db.session.add(self)
            db.session.commit()
            print(f"Notification created: {self.message}")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to create notification: {e}")

    def get_json(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "notification": self.message
        }

    def to_dict(self):
        return {
            "ID": self.id,
            "Student ID": self.student_id,
            "Notification": self.message
        }
    
    def __repr__(self):
        return f'<Notification {self.id} : {self.message}>'
