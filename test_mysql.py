# test_mysql.py
import MySQLdb

try:
    # Try to create a connection using your credentials
    connection = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Juliefang7",
        port=3306,
        db="er_triage_system"  # your database name
    )
    
    print("Successfully connected to MySQL!")
    
    # Get MySQL version
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MySQL version: {version[0]}")
    
    # Close connection
    connection.close()
    
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")