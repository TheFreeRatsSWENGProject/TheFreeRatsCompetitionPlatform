from App.database import db
from App.models import Moderator, Competition, Team, CompetitionTeam

def create_moderator(username, password):
    mod = get_mod_by_username(username)
    if mod:
        print(f'{username} already exists!')
        return None

    newMod = Moderator(username=username, password=password)
    try:
        db.session.add(newMod)
        db.session.commit()
        print(f'New Moderator: {username} created!')
        return newMod
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_mod_by_username(username):
    return Moderator.query.filter_by(username=username).first()

def get_mod(id):
    return Moderator.query.get(id)

def get_all_mods():
    return Moderator.query.all()

def get_all_mods_json():
    mods = Moderator.query.all()
    if not mods:
        return []
    mods_json = [mod.get_json() for mod in mods]
    return mods_json

def update_moderator(id, username):
    mod = get_mod(id)
    if mod:
        mod.username = username
        try:
            db.session.add(mod)
            db.session.commit()
            print("Username was updated!")
            return mod
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def add_mod(mod1_name, comp_name, mod2_name):
    mod1 = Moderator.query.filter_by(username=mod1_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    mod2 = Moderator.query.filter_by(username=mod2_name).first()

    if not mod1:
        print(f'Moderator: {mod1_name} not found!')
        return None
    else:
        if not comp:
            print(f'Competition: {comp_name} not found!')
            return None
        else: 
            if not mod2:
                print(f'Moderator: {mod2_name} not found!')
                return None
            else:
                return comp.add_mod(mod2)

def add_team(mod_name, comp_name, team):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    
    if not mod:
        print(f'Moderator: {mod_name} not found!')
        return None
    else:
        if not comp:
            print(f'Competition: {comp_name} not found!')
            return None
        else:
            """
            team = find_team(team_name, students)

            if not team:
                team = create_team(team_name, students)
            """
            if not team:
                print(f'Team was not created!')
                return None
            else:
                return comp.add_team(team)
                """
                comp_team = CompetitionTeam(comp_id=comp.id, team_id=team.id)
                try:
                    comp.teams.append(team)
                    team.competitions.append(comp)
                    db.session.add(comp)
                    db.session.add(team)
                    db.session.commit()
                    print(f'{team_name} added to {comp_name}!')
                    return comp_team
                except Exception as e:
                    db.session.rollback()
                    print(f'Something went wrong!')
                    return None
                """
                
