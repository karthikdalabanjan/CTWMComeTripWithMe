from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

db_url = settings.DATABASE_URL
connect_args = {}

# SQLite specific config
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
# PostgreSQL fix for postgres:// vs postgresql://
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def ensure_db_schema():
    """Ensures missing columns and tables in database are migrated safely."""
    try:
        from sqlalchemy import inspect, text
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        with engine.begin() as conn:
            if "users" in inspector.get_table_names():
                user_cols = [c["name"] for c in inspector.get_columns("users")]
                if "password_hash" not in user_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                if "avatar_url" not in user_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500)"))
                if "city" not in user_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN city VARCHAR(100) DEFAULT 'Bengaluru'"))
            if "bookings" in inspector.get_table_names():
                booking_cols = [c["name"] for c in inspector.get_columns("bookings")]
                if "itinerary_snapshot_json" not in booking_cols:
                    conn.execute(text("ALTER TABLE bookings ADD COLUMN itinerary_snapshot_json TEXT"))
    except Exception as e:
        print(f"Schema migration check notice: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
