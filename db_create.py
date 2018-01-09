from app import db

def db_create():
    db.create_all()

if __name__ == '__main__':
    db_create()
