from fastapi import FastAPI, Form, HTTPException, responses
import mysql.connector
import bcrypt

app = FastAPI()

@app.post("/login-validation")
async def login(user_email: str = Form(...), user_password: str = Form(...)):
    # 1. Connect to MySQL
    db = mysql.connector.connect(host="localhost", user="root", password="mysql", database="ConnectGo")
    cursor = db.cursor(dictionary=True) # dictionary=True makes it easier to read columns

    # 2. Check if email exists
    cursor.execute("SELECT password_hash, is_active FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()
    db.close()

    if not user:
        return responses.RedirectResponse(url="/signup", status_code=303)

    # 3. Check if account is banned/inactive
    if user['is_active'] == 0:
        return "Account is deactivated."

    # 4. Verify Password
    # We compare the PLAIN text password from the form 
    # against the HASHED password from the database
    if bcrypt.checkpw(user_password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        
        # 5. VALID: Redirect to the Dashboard
        return responses.RedirectResponse(url="/dashboard", status_code=302)
    
    else:
        # INVALID: Stay on login or show error
        return "Incorrect password!"