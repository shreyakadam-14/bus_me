# test_db_manager.py
from database_manager import DatabaseManager

print("Testing DatabaseManager...")
db = DatabaseManager()

# Check if we can connect
print(f"Database path: {db.db_path}")

# List all tables
tables = db.get_table_names()
print(f"\nFound {len(tables)} tables:")
for table in tables:
    print(f"  - {table}")

# Check users
users = db.fetch_all("SELECT username, role FROM users")
print(f"\nUsers in database: {len(users)}")
for user in users:
    print(f"  - {user['username']} ({user['role']})")

print("\n✓ DatabaseManager is working!")