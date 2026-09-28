from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.models import Role, RoleEnum, User


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for role_name in RoleEnum:
            if not db.query(Role).filter(Role.name == role_name).first():
                db.add(Role(name=role_name))
        db.commit()

        doctor_role = db.query(Role).filter(Role.name == RoleEnum.doctor).first()

        if not db.query(User).filter(User.email == "doctor@example.com").first():
            db.add(User(
                full_name="Demo Doctor",
                email="doctor@example.com",
                hashed_password=hash_password("Doctor@123"),
                role_id=doctor_role.id,
            ))
            db.commit()
            print("Created demo user")
    finally:
        db.close()