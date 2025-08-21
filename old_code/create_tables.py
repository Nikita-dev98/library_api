from database import engine, Base
import models

# This will create tables in your "library" DB if they don’t already exist
print("Creating tables in PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
