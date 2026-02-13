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

@app.get("/", response_class=responses.HTMLResponse)
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
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed))
        conn.commit()
        return {"message": "Success! User added to MySQL."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
        

@app.post("/login-validation")
async def login(user_email: str = Form(...), user_password: str = Form(...)):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password, is_active FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return responses.RedirectResponse(url="/signup", status_code=303)

    #active or not
    if user['is_active'] == 0:
        return "Account is deactivated."

    #password check
    if bcrypt.checkpw(user_password.encode('utf-8'), user['password'].encode('utf-8')):
        
        #Redirect to the Dashboard
        return responses.RedirectResponse(url="/dashboard", status_code=302)
    
    else:
        # INVALID
        return "Incorrect password!"