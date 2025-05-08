from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY
from models import db, User, UserPreference
from routes import routes  # Register blueprint for routes

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'  # Replace with .env in production

# ----------------- Configuration -----------------
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# ----------------- Initialize Extensions -----------------
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ----------------- User Authentication Setup -----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------- Register Blueprints -----------------
app.register_blueprint(routes)

# ----------------- Database Setup & Seeding -----------------
with app.app_context():
    db.create_all()

    # Create Admin (only if not exists)
    admin_email = "mandapatirenuka@gmail.com"
    admin_password = "admin123"
    
    if not User.query.filter_by(email=admin_email).first():
        hashed_pw = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        admin_user = User(username="Renuka", email=admin_email, password=hashed_pw, role="admin")
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully.")
    else:
        print("⚠️ Admin user already exists.")

    # Add preferences for a specific core user (Gopal)
    core_user = User.query.filter_by(email='gopal@gmail.com').first()
    if core_user and not UserPreference.query.filter_by(user_id=core_user.id).first():
        preference = UserPreference(
            user_id=core_user.id,
            preferred_category='cement',
            preferred_durability=8.5,
            budget=10000
        )
        db.session.add(preference)
        db.session.commit()
        print("✅ User preference added for Gopal.")
    else:
        print("⚠️ Preference already exists or user not found.")

# ----------------- Run Application -----------------
if __name__ == '__main__':
    print("✅ Database connected successfully!")
    app.run(debug=True)
