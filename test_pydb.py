import sys
import os
from datetime import datetime
from disk_db.pydb import MultiThreadedDatabase

# Initialize the database
db = MultiThreadedDatabase("test_db")

# Create the 'users' table with columns: id, name, age, created_at
db.create_table("users", ["id", "name", "age", "created_at"], primary_key="id")

# Insert some data into the users table
users_table = db.get_table("users")
users_table.insert({"id": 1, "name": "Alice", "age": 30, "created_at": str(datetime.now())})
users_table.insert({"id": 2, "name": "Bob", "age": 24, "created_at": str(datetime.now())})
users_table.insert({"id": 3, "name": "Charlie", "age": 28, "created_at": str(datetime.now())})

# Save the data
users_table.save()

# Query to select all users
query = "SELECT * FROM users"
results = db.execute_query(query)
print("All Users:", results)

# Query to select users with age greater than 25
query = "SELECT * FROM users WHERE age > 25"
results = db.execute_query(query)
print("Users with age > 25:", results)

# Update a user (e.g., change name of user with id = 1)
query = "UPDATE users SET name = 'Alice Cooper' WHERE id = 1"
db.execute_query(query)

# Verify the update
query = "SELECT * FROM users WHERE id = 1"
results = db.execute_query(query)
print("Updated User:", results)

# Delete a user (e.g., delete user with id = 2)
query = "DELETE FROM users WHERE id = 2"
db.execute_query(query)

# Verify deletion by selecting all users
query = "SELECT * FROM users"
results = db.execute_query(query)
print("Remaining Users:", results)
