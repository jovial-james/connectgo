from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import mysql.connector
import bcrypt

app = FastAPI()


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="ConnectGo"
    )

@app.get("/", response_class=HTMLResponse)
async def signup_page():
    # This serves a simple HTML form to the user
    return """
    <html>
        <body>
            <h2>Create Account</h2>
            <form action="/register" method="post">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="email" name="email" placeholder="Email"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <button type="submit">Sign Up</button>
            </form>
        </body>
    </html>
    """

@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 1. Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 2. Use your mysql-connector logic
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                       (username, email, hashed))
        conn.commit()
        return {"message": "Success! User added to MySQL."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()