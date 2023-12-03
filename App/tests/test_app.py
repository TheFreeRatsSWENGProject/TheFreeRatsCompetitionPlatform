import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

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
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

#Student Unit Tests
    def test_new_student(self):
      db.drop_all()
      db.create_all()
      student = Student("bob", "bobpass")
      assert student.username == "bob"

    def test_student_get_json(self):
      db.drop_all()
      db.create_all()
      student = Student("bob", "bobpass")
      self.assertDictEqual(student.get_json(), {"id": None, "username":"bob", "role": 'Student'})

#Host Unit Tests
    def test_new_host(self):
      db.drop_all()
      db.create_all()
      host = Host("bill", "billpass", 101)
      assert host.username == "bill" and host.host_id == 101

    def test_host_get_json(self):
      db.drop_all()
      db.create_all()
      host = Host("bill", "billpass", 101)
      self.assertDictEqual(host.get_json(), {"id":None, "username":"bill", "role": 'Host', "host id": 101, "competitions": []})

#Admin Unit Tests
    def test_new_admin(self):
      db.drop_all()
      db.create_all()
      admin = Admin("rob", "robpass", 1001)
      assert admin.username == "rob" and admin.staff_id == 1001

    def test_admin_get_json(self):
      db.drop_all()
      db.create_all()
      admin = Admin("rob", "robpass", 1001)
      self.assertDictEqual(admin.get_json(), {"id":None, "username":"rob", "role": 'Admin', "staff_id": 1001})

#Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime")
      assert competition.name == "RunTime"

    def test_competition_get_json(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime")
      self.assertDictEqual(competition.get_json(), {"id": None,"name": "RunTime", "hosts": [], "participants": []})

'''
    Integration Tests
'''
class IntegrationTests(unittest.TestCase):

#Create Competition Integration Tests
    def test1_create_competition(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      comp = create_competition("RunTime", 101)
      assert comp.name == "RunTime"

    def test2_create_competition(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      assert create_competition("CodeSprint", 100) == None
   
#Display Student Info Integration Tests
    def test_display_student_info(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      comp = create_competition("RunTime", 101)
      student = create_student("bob", "bobpass")
      student_rank = create_ranking(student.id)
      register_student("bob", "RunTime")
      host = create_host("rob", "robpass", 1001)
      join_comp("rob", "RunTime")
      add_results("rob", "bob", "RunTime", 15)
      update_rankings()
      self.assertDictEqual(display_student_info("bob"), {"profile": {'id': 1, 'username': 'bob', 'role': 'Student'}, "ranking": {'rank': 1, 'total points': 15}, "participated_competitions": ['RunTime']})

'Display Notification Integration Tests
    def test_display_notification(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      comp = create_competition("RunTime", 101)
      student = create_student("bob", "bobpass")
      student_rank = create_ranking(student.id)
      register_student("bob", "RunTime")
      host = create_host("rob", "robpass", 1001)
      join_comp("rob", "RunTime")
      add_results("rob", "bob", "RunTime", 15)
      update_rankings()
      self.assertDictEqual(display_notifications("bob"), {"notifications": [{"id": 1, "notification": "Ranking changed from Unranked to 1"}]})

    #Additional Integration Tests
    def test_create_student(self):
      db.drop_all()
      db.create_all()
      student = create_student("bob", "bobpass")
      assert student.username == "bob"

    def test_create_host(self):
      db.drop_all()
      db.create_all()
      host = create_host("rob", "robpass", 101)
      assert host.username == "rob" and host.host_id == 101
  
    def test_create_admin(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 1001)
      assert admin.username == "bill" and admin.staff_id == 1001

    def test_student_list(self):
      db.drop_all()
      db.create_all()
      ben = create_student('ben', 'benpass')
      sally = create_student('sally', 'sallypass')
      bob = create_student('bob', 'bobpass')
      jake = create_student('jake', 'jakepass')
      amy = create_student('amy', 'amypass')
      students = get_all_students_json()
      
      self.assertEqual(students, [{'id': 1, 'username': 'ben', 'role': 'Student'}, {'id': 2, 'username': 'sally', 'role': 'Student'}, {'id': 3, 'username': 'bob', 'role': 'Student'}, {'id': 4, 'username': 'jake', 'role': 'Student'}, {'id': 5, 'username': 'amy', 'role': 'Student'}])

    def test_comp_list(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      comp1 = create_competition("CodeSprint", 101)
      comp2 = create_competition("RunTime", 101)
      comp3 = create_competition("HashCode", 101)
      comps = get_all_competitions_json()

      self.assertListEqual(comps, [{"id":1, "name":"CodeSprint", "hosts": [], "participants": []}, {"id":2, "name":"RunTime", "hosts": [], "participants": []}, {"id":3, "name":"HashCode", "hosts": [], "participants": []}])
    
   def test1_register_student(self):
      db.drop_all()
      db.create_all()
      admin = create_admin("bill", "billpass", 101)
      comp = create_competition("RunTime", 101)
      student = create_student("bob", "bobpass")
      assert register_student("bob", "RunTime") != None

