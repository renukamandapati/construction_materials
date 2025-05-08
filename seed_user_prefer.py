from app import app
from models import db, User, UserPreference

# Always perform database operations within the app context
with app.app_context():
    # Find the user by email
    user = User.query.filter_by(email='gopal@gmail.com').first()

    if user:
        # Check if the user already has a preference set
        existing_pref = UserPreference.query.filter_by(user_id=user.id).first()

        if not existing_pref:
            # If no preference exists, create a new one
            new_preference = UserPreference(
                user_id=user.id,
                preferred_category='cement',
                preferred_durability=8.5,
                budget=10000
            )
            db.session.add(new_preference)
            print("✅ User preference created successfully.")
        else:
            # If preference already exists, update the existing record
            existing_pref.preferred_category = 'cement'
            existing_pref.preferred_durability = 8.5
            existing_pref.budget = 10000
            print("✅ User preference updated successfully.")

        # Save the changes to the database
        db.session.commit()
