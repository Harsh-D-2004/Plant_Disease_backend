from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Database connected")
    finally:
        db.close()