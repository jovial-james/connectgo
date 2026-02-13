from fastapi import FastAPI, Form, responses
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

@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed))
        conn.commit()
        # FIX 1: Redirect on success so the user can actually login
        return responses.RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.post("/login-validation")
async def login(user_email: str = Form(...), user_password: str = Form(...)):
    conn = get_db_connection()
    # FIX 2: Added dictionary=True
    cursor = conn.cursor(dictionary=True) 

    cursor.execute("SELECT password, is_active FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        # Note: Your route is @app.get("/"), so redirect to "/" not "/signup"
        return responses.RedirectResponse(url="/", status_code=303)

    if user['is_active'] == 0:
        return "Account is deactivated."

    # FIX 3: Ensure the stored password is treated as bytes for bcrypt
    stored_password = user['password']
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')

    if bcrypt.checkpw(user_password.encode('utf-8'), stored_password):
        return responses.RedirectResponse(url="/dashboard", status_code=302)
    else:
        return "Incorrect password!"