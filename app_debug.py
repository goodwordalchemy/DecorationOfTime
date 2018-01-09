from app import app
from db_create import db_create

if __name__ == '__main__':
    db_create()
    app.run(debug=True)
