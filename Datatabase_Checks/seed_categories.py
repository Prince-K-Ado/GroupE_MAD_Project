from app import app, db
from app.models import Category

categories = [
    "Disaster Relief", "Health", "Education", "Environment", 
    "Animal Welfare", "Community Development", "Food", "Hospital Bills", 
    "Refugees Assistance"
]

with app.app_context():
    for cat in categories:
        if not Category.query.filter_by(name=cat).first():
            new_cat = Category(name=cat)
            db.session.add(new_cat)
    db.session.commit()
    print("Categories seeded!")