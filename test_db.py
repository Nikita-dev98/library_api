from database import engine, Base
import psycopg2

# Optional: Test SQLAlchemy connection by creating tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ SQLAlchemy connected and tables can be created!")
except Exception as e:
    print("❌ SQLAlchemy connection failed:", e)

# Optional: Test direct psycopg2 connection
try:
    conn = psycopg2.connect(
        dbname="library",
        user="library_user",
        password="qwerty",
        host="localhost",
        port="5432"
    )
    print("✅ psycopg2 connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("❌ psycopg2 connection failed:", e)
