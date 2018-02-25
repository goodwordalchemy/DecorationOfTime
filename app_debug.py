from app import app, mongo

if __name__ == '__main__':
    with app.app_context():
        db = mongo.db

    db.users.drop()

    app.run(debug=True)
