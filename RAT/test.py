import mysql.connector as sql
import random

# Connect to the database
con = sql.connect(host='localhost', 
                  user='root',
                  passwd='1234',
                  database='temp')
print("CONNECTED !")
print()

# Create a cursor object
cursor = con.cursor()

# Define the SQL query
sql_query = "INSERT INTO server VALUES (%s, %s)"

# Insert random values into the database
for i in range(5):    
    a = random.randint(123, 255)
    b = random.randint(123, 255)
    c = random.randint(123, 255)
    d = random.randint(123, 255)
    ip = f"{a}.{b}.{c}.{d}"
    state = random.choice(["Online", None])  # Use random.choice to get a single element
    val = (ip, state)
    
    # Execute the SQL query
    cursor.execute(sql_query, val)
    print(f"Inserted value {i}")

# Commit the transaction
con.commit()

# Close the connection
cursor.close()
con.close()
