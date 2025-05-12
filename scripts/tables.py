import pymysql

DB_HOST = 'triinuliist.mysql.eu.pythonanywhere-services.com'
DB_USER = 'triinuliist'
DB_PASSWORD = 'KoorilauluApp25'
DB_NAME = 'triinuliist$koorilauluapp'

# Connect to the database
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()

# SQL query to create a new table
create_table_query = """
CREATE TABLE if not exists laulud (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nimi VARCHAR(100) NOT NULL,
    failitee VARCHAR(100) UNIQUE NOT NULL,
    partii VARCHAR(100) NOT NULL
);
"""

# Execute the query
cursor.execute(create_table_query)

# Commit changes
connection.commit()

print('tabel loodud')

# Close the connection
cursor.close()
connection.close()