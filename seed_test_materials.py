from app import app
from models import db, Material, Supplier

# Always work inside the app context to interact with the database
with app.app_context():
    # Check if any supplier exists
    supplier = Supplier.query.first()

    if not supplier:
        # If no supplier found, create a default supplier
        supplier = Supplier(
            name='Test Supplier',
            contact='9876543210'
        )
        db.session.add(supplier)
        db.session.commit()

    # Check if the material 'Ultra Cement' already exists
    existing_material = Material.query.filter_by(name='Ultra Cement').first()

    if not existing_material:
        # If not found, add 'Ultra Cement' to the database
        new_material = Material(
            name='Ultra Cement',
            category='cement',
            price=9800,
            durability=9.0,   # Make sure durability is stored as float
            supplier_id=supplier.id  # Link the material to the supplier
        )
        db.session.add(new_material)
        db.session.commit()
        print("✅ 'Ultra Cement' material has been added to the database.")
    else:
        print("ℹ️ 'Ultra Cement' already exists in the database.")
