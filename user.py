import mysql.connector
import bcrypt

def create_user(username, email, plain_password):
    try:
        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="ConnectGo"
        )
        cursor = db.cursor()

        #Hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, hashed)

        cursor.execute(sql, values) 
       
        db.commit()
        print(f"User {username} created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()