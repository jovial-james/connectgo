import mysql.connector
import os

try:
    conn=mysql.connector.connect(host=os.getenv("10.70.246.154"), user=os.getenv("root"), password=os.getenv("mysql"),port=int(os.getenv("DB_PORT", 3306))
    cursor = conn.cursor()
    cursor.execute("create database if not exists ConnectGo")
    cursor.execute("use ConnectGo")

    #create tables

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    destination VARCHAR(100) NOT NULL,
    description TEXT,
    departure_date DATE,
    duration_days INT,
    budget_level ENUM('low', 'medium', 'high'),
    travel_type ENUM('individual', 'family', 'group'),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS saved_plans (
    save_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    trip_id INT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE
    )""")
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    content TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
    )""")
    conn.commit()

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

