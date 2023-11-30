from App.database import db

class CompetitionHost(db.Model):
    __tablename__='competition_host'

    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    host_id =  db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)

    def __init__(self, comp_id, host_id):
      self.comp_id = comp_id
      self.host_id = host_id
      
    def get_json(self):
      return {
        'id': self.id,
        'comp_id': self.comp_id,
        'host_id': self.host_id
      }

    def to_Dict(self):
      return {
        'id': self.id,
        'comp_id': self.comp_id,
        'host_id': self.host_id
      }