"""
Run once after first starting the backend to create the three roles and
a demo doctor login you can use immediately:

    email: doctor@example.com
    password: Doctor@123

Usage (from backend/, with venv active):
    python seed_db.py
"""
from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.models import Role, RoleEnum, User

Base.metadata.create_all(bind=engine)

db = SessionLocal()

for role_name in RoleEnum:
    if not db.query(Role).filter(Role.name == role_name).first():
        db.add(Role(name=role_name))
db.commit()

doctor_role = db.query(Role).filter(Role.name == RoleEnum.doctor).first()

if not db.query(User).filter(User.email == "doctor@example.com").first():
    demo_user = User(
        full_name="Demo Doctor",
        email="doctor@example.com",
        hashed_password=hash_password("Doctor@123"),
        role_id=doctor_role.id,
    )
    db.add(demo_user)
    db.commit()
    print("Created demo user: doctor@example.com / Doctor@123")
else:
    print("Demo user already exists.")

db.close()
print("Seed complete.")
