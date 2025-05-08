import csv
from app import app, db
from models import Material

with app.app_context():
    with open('datasets/materials.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            material = Material(
                id=int(row['id']),
                name=row['name'],
                category=row['category'],
                price=float(row['price']),
                durability=row['durability'],
                supplier_id=int(row['supplier_id'])
            )
            db.session.add(material)
        db.session.commit()
    print("Materials data imported successfully.")
