import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",      
            user="root",          
            password="",           
            database="voting" 
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None
