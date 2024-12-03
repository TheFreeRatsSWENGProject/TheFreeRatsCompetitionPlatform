import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass")
        assert user.username == "ryan"

    def test_hashed_password(self):
        password = "ryanpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("ryan", password)
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      student = Student("james", "jamespass")
      assert student.username == "james"

    def test_student_get_json(self):
      student = Student("james", "jamespass")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})

    #Moderator Unit Tests
    def test_new_moderator(self):
      mod = Moderator("robert", "robertpass")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self): 
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      expected_json = { 
          "id": None,  # There is no ID since the constructor did not pass one and that the database auto assigns a consecutive number as the ID for the competition;
                       # since there is no db.add(competition) db.commit(), there is no ID being assigned.
          "name": "RunTime", 
          "date": "09-02-2024",  # This matches the format used in get_json
          "location": "St. Augustine", 
          "level": 1, 
          "max_score": 25, 
          "confirm": False,  # Include the confirm field
          "moderators": [],  # No moderators added
          "teams": []  # No teams added
      } 
      actual_json = competition.get_json() 
      self.assertDictEqual(actual_json, expected_json)
    
    #Notification Unit Tests
    def test_new_notification(self):
      notification = Notification(1, "Ranking changed!")
      assert notification.student_id == 1 and notification.message == "Ranking changed!"

    def test_notification_get_json(self):
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})

    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      competition_team.update_rating(12)
      self.assertDictEqual(competition_team.get_json(), {"id": None, "team_id": 1, "competition_id": 1, "points_earned": 15, "rating_score": 12})

    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
        competition_moderator = CompetitionModerator(comp_id=1, mod_id=1)
        # db.session.add(competition_moderator)
        # db.session.commit()
        expected_json = {
            'id': None, # No ID expected since this field is auto-populated once added to the database;
            'competition_id': 1,
            'moderator_id': 1
        }
        self.assertDictEqual(competition_moderator.get_json(), expected_json)

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})

'''
    Integration Tests
'''
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class IntegrationTests(unittest.TestCase):
    # Setup: Calls this method before every test is executed
    def setUp(self):
        db.drop_all()
        db.create_all()

    #Feature 1 Integration Tests
    def test1_create_competition(self):
        db.drop_all()
        db.create_all()
        mod = create_moderator("debra", "debrapass")
        comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        assert comp is not None
        
        expected_json = {
            "id": comp.id,
            "name": "RunTime",
            "date": "29-03-2024",
            "location": "St. Augustine",
            "level": 2,
            "max_score": 25,
            "confirm": False,
            "moderators": ["debra"],
            "teams": []
        }
        
        actual_json = comp.get_json()
        
        assert actual_json == expected_json

    def test2_create_competition(self):
        db.drop_all()
        db.create_all()
        mod = create_moderator("debra", "debrapass")
        comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        self.assertIsNotNone(comp)
        expected_json = {
            "id": comp.id,
            "name": "RunTime",
            "date": "29-03-2024",
            "location": "St. Augustine",
            "level": 2,
            "max_score": 25,
            "confirm": False,
            "moderators": ["debra"],
            "teams": []
        }
        self.assertDictEqual(comp.get_json(), expected_json)
      
    #Feature 2 Integration Tests
    def test1_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      assert comp_team.points_earned == 15
    
    def test2_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      students = [student1.username, student2.username, student3.username]
      add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students = [student1.username, student4.username, student5.username]
      team = add_team(mod.username, comp.name, "Scrum Lords", students)
      assert team == None
    
    def test3_add_results(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod2.username, comp.name, "Runtime Terrors", students)
      assert team == None

    #Feature 3 Integration Tests
    def test_display_student_info(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertDictEqual(display_student_info("james"), {"profile": {'id': 1, 'username': 'james', 'rating_score': 24.0, 'comp_count': 1, 'curr_rank': 1}, "competitions": ['RunTime']})

    #Feature 4 Integration Tests
    def test_display_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      student7 = create_student("isabella", "isabellapass")
      student8 = create_student("richard", "richardpass")
      student9 = create_student("jessica", "jessicapass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 12)
      students3 = [student7.username, student8.username, student9.username]
      team3 = add_team(mod.username, comp.name, "Beyond Infinity", students3)
      comp_team = add_results(mod.username, comp.name, "Beyond Infinity", 10)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertDictEqual(comp.get_json(), {'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'confirm': True, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords', 'Beyond Infinity']})

    #Feature 5 Integration Tests
    def test_display_rankings(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertListEqual(display_rankings(), [{"placement": 1, "student": "james", "rating score": 24.0}, {"placement": 1, "student": "steven", "rating score": 24.0}, {"placement": 1, "student": "emily", "rating score": 24.0}, {"placement": 4, "student": "mark", "rating score": 16.0}, {"placement": 4, "student": "eric", "rating score": 16.0}, {"placement": 4, "student": "ryan", "rating score": 16.0}])

    def test_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      update_ratings(mod.username, comp.name)
      test=display_notifications("james")
      print(test)
      self.assertDictEqual(display_notifications("james"), {'notifications': [{'ID': 3, 'Student ID': 1, 'Notification': 'RANK : 1. Congratulations on your first rank!'}]})

    #Feature 6 Integration Tests
    def test1_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp.name)
      print(display_notifications("james"))
      self.assertDictEqual(display_notifications("james"), {'notifications': [{'ID': 3, 'Student ID': 1, 'Notification': 'RANK : 1. Congratulations on your first rank!'}]})

    def test2_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      print("ALL STUDENTS MADE")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      print("COMP 1 FINISH")
      print(display_notifications("james"))
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 15)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      print("COMP 2 FINISH")
      print(display_notifications("james"))
      self.assertDictEqual(display_notifications("james"), {'notifications': [{'ID': 3, 'Student ID': 1, 'Notification': 'RANK : 1. Congratulations on your first rank!'}, {'ID': 9, 'Student ID': 1, 'Notification': 'RANK : 1. Well done! You retained your rank.'}]})

    def test3_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      test=display_notifications("steven")
      print(test)
      self.assertDictEqual(display_notifications("steven"), {'notifications': [{'ID': 2, 'Student ID': 2, 'Notification': 'RANK : 1. Congratulations on your first rank!'}, {'ID': 8, 'Student ID': 2, 'Notification': 'RANK : 1. Well done! You retained your rank.'}, {'ID': 16, 'Student ID': 2, 'Notification': 'RANK : 4. Oh no! Your rank has went down.'}]})

    def test4_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      test=display_notifications("mark")
      print(test)
      self.assertDictEqual(display_notifications("mark"), {'notifications': [{'ID': 6, 'Student ID': 4, 'Notification': 'RANK : 4. Congratulations on your first rank!'}, {'ID': 12, 'Student ID': 4, 'Notification': 'RANK : 4. Well done! You retained your rank.'}, {'ID': 14, 'Student ID': 4, 'Notification': 'RANK : 2. Congratulations! Your rank has went up.'}]})

    #Additional Integration Tests
    def test_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      mod3 = create_moderator("raymond", "raymondpass")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      assert add_mod(mod2.username, comp.name, mod3.username) == None
    
    def test_student_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      test= get_all_students_json()
      print(test)
      self.assertEqual(get_all_students_json(), [{'id': 1, 'username': 'james', 'rating_score': 22, 'comp_count': 2, 'curr_rank': 1}, {'id': 2, 'username': 'steven', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 3, 'username': 'emily', 'rating_score': 17, 'comp_count': 2, 'curr_rank': 4}, {'id': 4, 'username': 'mark', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 5, 'username': 'eric', 'rating_score': 18, 'comp_count': 2, 'curr_rank': 2}, {'id': 6, 'username': 'ryan', 'rating_score': 13, 'comp_count': 2, 'curr_rank': 6}])

    def test_comp_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      print("ALL STUDENTS MADE")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      test= get_all_competitions_json()
      print(test)
      self.assertListEqual(get_all_competitions_json(), [{'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'confirm': True, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords']}, {'id': 2, 'name': 'Hacker Cup', 'date': '23-02-2024', 'location': 'Macoya', 'level': 1, 'max_score': 20, 'confirm': True, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords']}])

    def test_get_rank_history(self):
        mod = create_moderator("debra", "debrapass")
        comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
        comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30)
        student1 = create_student("james", "jamespass")
        student2 = create_student("steven", "stevenpass")
        student3 = create_student("emily", "emilypass")
        students1 = [student1.username, student2.username, student3.username]
        team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
        comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
        update_ratings(mod.username, comp1.name)
        update_rankings(comp1.name)

        students2 = [student1.username, student2.username, student3.username]
        team2 = add_team(mod.username, comp2.name, "Scrum Lords", students2)
        comp2_team2 = add_results(mod.username, comp2.name, "Scrum Lords", 20)
        update_ratings(mod.username, comp2.name)
        update_rankings(comp2.name)

        rank_history = get_rank_history_json(student2.username)
        print(rank_history)

        self.assertListEqual(get_rank_history_json("steven"), [{'student_id': 2, 'rank': 1, 'date': '2024-03-29', 'score': 24.0}, {'student_id': 2, 'rank': 1, 'date': '2024-03-29', 'score': 24.0}, {'student_id': 2, 'rank': 1, 'date': '2024-02-23', 'score': 18.666666666666664}, {'student_id': 2, 'rank': 1, 'date': '2024-02-23', 'score': 18.666666666666664}])

if __name__ == '__main__':
    unittest.main()