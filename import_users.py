from models import db, User
from flask_bcrypt import Bcrypt
from app import app
import csv

bcrypt = Bcrypt()

with app.app_context():
    with open('datasets/user.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_user = User.query.filter_by(email=row['email']).first()
            if not existing_user:
                hashed_password = bcrypt.generate_password_hash(row['admin123']).decode('utf-8')
                new_user = User(
                    username=row['username'],
                    email=row['email'],
                    password=hashed_password,
                    role=row['role']
                )
                db.session.add(new_user)
        db.session.commit()
