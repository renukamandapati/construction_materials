import csv
from app import app, db
from models import Project

with app.app_context():
    with open('datasets/projects.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            project = Project(
                id=int(row['id']),
                project_name=row['project_name'],
                material_id=int(row['material_id']),
                supplier_id=int(row['supplier_id'])
            )
            db.session.add(project)
        db.session.commit()
    print("Projects data imported successfully.")
