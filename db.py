import mysql.connector
try:
    conn=mysql.connector.connect(host='localhost',user="root",password="mysql")
    cursor = conn.cursor()
    cursor.execute("create database ConnectGo")
    cursor.execute("use ConnectGo")

    #create tables
    cursor.execute("""CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1
    )""")
    conn.commit()
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

