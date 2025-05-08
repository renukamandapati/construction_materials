from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Material, UserPreference

bcrypt = Bcrypt()
routes = Blueprint('routes', __name__)

# HOME PAGE
@routes.route('/')
def home():
    return render_template('index.html')

# USER REGISTRATION
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        selected_role = request.form['role']

        role = 'core_user'  # Default role

        if selected_role == 'admin':
            if email == "mandapatirenuka@gmail.com":
                role = 'admin'
            else:
                flash("You're not authorized to register as an admin. Registered as core user.", "warning")

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('routes.login'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# USER LOGIN
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# USER LOGOUT
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# DASHBOARD
@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# VIEW ALL MATERIALS
@routes.route('/view_materials')
@login_required
def view_materials():
    materials = Material.query.all()
    return render_template('view_materials.html', materials=materials)

#RECOMMEND MATERIALS
@routes.route('/recommend_materials')
@login_required
def recommend_materials():
    user_pref = UserPreference.query.filter_by(user_id=current_user.id).first()

    # Case 1: No preference row at all
    if not user_pref:
        flash('⚠️ You have not set your preferences yet. Please set them first!', 'warning')
        return redirect(url_for('routes.set_preferences'))

    # Case 2: Preference exists, but data is empty or invalid
    if (
        not user_pref.preferred_category or user_pref.preferred_category.strip() == "" or
        user_pref.preferred_durability is None or
        user_pref.budget is None or
        user_pref.budget <= 0 or
        user_pref.preferred_durability <= 0
    ):
        flash('⚠️ Your preferences are incomplete or invalid. Please update them!', 'warning')
        return redirect(url_for('routes.set_preferences'))

    # All good, fetch recommendations
    materials = Material.query.filter(
        Material.category == user_pref.preferred_category,
        Material.price <= user_pref.budget,
        Material.durability >= user_pref.preferred_durability
    ).all()

    return render_template('recommend_materials.html', preference=user_pref, materials=materials, username=current_user.username)

#ADD MATERIALS
@routes.route('/add_material', methods=['GET', 'POST'])
@login_required
def add_material():
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            category = request.form['category'].strip()
            price = float(request.form['price'])
            durability = float(request.form['durability'])
            supplier_id = int(request.form['supplier_id'])

            new_material = Material(name=name, category=category, price=price, durability=durability, supplier_id=supplier_id)
            db.session.add(new_material)
            db.session.commit()
            flash("Material added successfully!", "success")
            return redirect(url_for('routes.view_materials'))
        except Exception as e:
            flash(f"Error adding material: {e}", "danger")

    return render_template('add_material.html')


# SET / UPDATE PREFERENCES
@routes.route('/set_preferences', methods=['GET', 'POST'])
@login_required
def set_preferences():
    preference = UserPreference.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        try:
            category = request.form['preferred_category']
            durability = float(request.form['preferred_durability'])
            budget = int(request.form['budget'])

            if preference:
                preference.preferred_category = category
                preference.preferred_durability = durability
                preference.budget = budget
            else:
                preference = UserPreference(
                    user_id=current_user.id,
                    preferred_category=category,
                    preferred_durability=durability,
                    budget=budget
                )
                db.session.add(preference)

            db.session.commit()
            flash('Preferences saved successfully!', 'success')
            return redirect(url_for('routes.dashboard'))

        except (KeyError, ValueError):
            flash('Invalid input values. Please check your form.', 'danger')

    return render_template('set_preferences.html')

# EDIT MATERIAL (Admin Only)
@routes.route('/edit_material/<int:material_id>', methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('routes.dashboard'))

    material = Material.query.get_or_404(material_id)

    if request.method == 'POST':
        material.name = request.form['name']
        material.category = request.form['category']
        material.price = float(request.form['price'])
        material.durability = float(request.form['durability'])
        material.supplier_id = int(request.form['supplier_id'])

        db.session.commit()
        flash("Material updated successfully!", "success")
        return redirect(url_for('routes.view_materials'))

    return render_template('edit_material.html', material=material)

# DELETE MATERIAL (Admin Only)
@routes.route('/delete_material/<int:material_id>', methods=['POST'])
@login_required
def delete_material(material_id):
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('routes.dashboard'))

    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash("Material deleted successfully!", "success")
    return redirect(url_for('routes.view_materials'))
