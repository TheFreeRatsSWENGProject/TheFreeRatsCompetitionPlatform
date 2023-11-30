from App.models import Host, Competition, Student, Ranking
from App.models.competition_student import *
from App.database import db
from App.controllers import Ranking

def create_host(username, password, host_id):
    host = get_host_by_username(username)
    if host:
        print(f'{username} already exists!')
        return None

    newHost = Host(username=username, password=password, host_id=host_id)
    try:
        db.session.add(newHost)
        db.session.commit()
        print(f'New Host: {username} created!')
        return newHost
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_host_by_username(username):
    return Host.query.filter_by(username=username).first()

def get_host(id):
    return Host.query.get(id)

def get_all_hosts():
    return Host.query.all()

def get_all_hosts_json():
    hosts = Host.query.all()
    if not hosts:
        return []
    hosts_json = [host.get_json() for host in hosts]
    return hosts_json

def update_host(id, username):
    host = get_host(id)
    if host:
        host.username = username
        try:
            db.session.add(host)
            db.session.commit()
            print("Username was updated!")
            return host
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None