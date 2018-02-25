from app import app, mongo

with app.app_context():
    db = mongo.db

results = list(db.users.find())

print(results)
