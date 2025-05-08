from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

# ---------------------- USER MODEL ----------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='core_user')  # 'admin' or 'core_user'

    # One-to-one relationship: each user can have one preference
    preference = db.relationship('UserPreference', back_populates='user', uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"

# ---------------------- MATERIAL MODEL ----------------------
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    durability = db.Column(db.String(50), nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    supplier = db.relationship('Supplier', backref='materials', lazy=True)

    def __repr__(self):
        return f"<Material {self.name}>"

# ---------------------- SUPPLIER MODEL ----------------------
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Supplier {self.name}>"

# ---------------------- PROJECT MODEL ----------------------
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)

    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    def __repr__(self):
        return f"<Project {self.project_name}>"

# USER PREFERENCES MODEL
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    preferred_category = db.Column(db.String(100), nullable=False)
    preferred_durability = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    # One-to-one back-reference to user
    user = db.relationship('User', back_populates='preference')

    def __repr__(self):
        return f"<UserPreference user_id={self.user_id}, category={self.preferred_category}, durability={self.preferred_durability}, budget={self.budget}>"
