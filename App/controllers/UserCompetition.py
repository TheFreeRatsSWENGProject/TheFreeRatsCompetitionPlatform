from App.models import Competition, User, competition_student
from App.database import db

def findCompUser(user_id, comp_id):
    user = UserCompetition.query.get(user_id)

    if user:
        comp = user.query.get(comp_id)
        if comp:
            print("yay")
            return True
    
    print("no bueno")
    return False