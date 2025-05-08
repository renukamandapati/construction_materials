import csv
from app import app, db
from models import Supplier

with app.app_context():
    with open('datasets/suppliers.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            supplier = Supplier(
                id=int(row['id']),
                name=row['name'],
                contact=row['contact']
            )
            db.session.add(supplier)
        db.session.commit()
    print("Suppliers data imported successfully.")
