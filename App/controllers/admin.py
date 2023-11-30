from App.models import Admin
from App.database import db

def create_admin(username, password, staff_id):
    admin = get_admin_by_username(username)
    if admin:
        print(f'{username} already exists!')
        return None

    newAdmin = Admin(username=username, password=password, staff_id=staff_id)
    try:
        db.session.add(newAdmin)
        db.session.commit()
        print(f'New Admin: {username} created!')
        return newAdmin
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()

def get_admin(id):
    return Admin.query.get(id)

def get_all_admins():
    return Admin.query.all()

def get_all_admins_json():
    admins = Admin.query.all()
    if not admins:
        return []
    admins_json = [admin.get_json() for admin in admins]
    return admins_json

def update_admin(id, username):
    admin = get_admin(id)
    if admin:
        admin.username = username
        try:
            db.session.add(admin)
            db.session.commit()
            print("Username was updated!")
            return admin
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None