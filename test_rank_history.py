from App import create_app, db
from App.models import Student, RankHistory

def check_rank_history(username):
    app = create_app()
    app.app_context().push()

    student = Student.query.filter_by(username=username).first()
    if student:
        history = RankHistory.query.filter_by(student_id=student.id).order_by(RankHistory.contest_date.desc()).all()
        if history:
            print(f"Rank history for {username}:")
            print("Rank\tDate")
            for entry in history:
                print(f"{entry.rank}\t{entry.contest_date}")
        else:
            print(f"No rank history found for {username}.")
    else:
        print(f"Student '{username}' not found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python test_rank_history.py <username>")
    else:
        check_rank_history(sys.argv[1])