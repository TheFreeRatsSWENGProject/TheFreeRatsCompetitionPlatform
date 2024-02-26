from App.database import db

class CompetitionAdmin(db.Model):
    __tablename__='competition_admin'

    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    admin_id =  db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, comp_id, admin_id):
      self.comp_id = comp_id
      self.admin_id = admin_id
      
    def get_json(self):
      return {
        'id': self.id,
        'competition_id': self.comp_id,
        'admin_id': self.admin_id
      }

    def to_Dict(self):
      return {
        'ID': self.id,
        'Competition ID': self.comp_id,
        'Admin ID': self.admin_id
      }