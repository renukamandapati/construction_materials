import csv
from app import app, db
from models import UserPreference

with app.app_context():
    with open('datasets/user_preferences.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pref = UserPreference(
                id=int(row['id']),
                user_id=int(row['user_id']),
                material_id=int(row['material_id'])
            )
            db.session.add(pref)
        db.session.commit()
    print("User preferences imported successfully.")
