from app import app, db
from models.user import User


with app.app_context():

    existing_user = User.query.filter_by(
        username="admin"
    ).first()

    if existing_user:

        print("Admin user already exists.")

    else:

        admin = User(
            username="admin",
            role="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")