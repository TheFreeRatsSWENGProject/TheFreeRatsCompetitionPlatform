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

'Student Unit Tests
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

'''
    Integration Tests
'''
class IntegrationTests(unittest.TestCase):

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

    
