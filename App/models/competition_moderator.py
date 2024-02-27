from App.database import db

class CompetitionModerator(db.Model):
    __tablename__='competition_moderator'

    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    mod_id =  db.Column(db.Integer, db.ForeignKey('moderator.id'), nullable=False)

    def __init__(self, comp_id, mod_id):
      self.comp_id = comp_id
      self.mod_id = mod_id
      
    def get_json(self):
      return {
        'id': self.id,
        'competition_id': self.comp_id,
        'moderator_id': self.mod_id
      }

    def to_Dict(self):
      return {
        'ID': self.id,
        'Competition ID': self.comp_id,
        'Moderator ID': self.mod_id
      }