from fastapi import FastAPI, Form, responses, Request
import mysql.connector
import bcrypt
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),     
        user=os.getenv("DB_USER"),      
        password=os.getenv("DB_PASSWORD"), 
        database="ConnectGo",
        port=int(os.getenv("DB_PORT", 3306))
    )

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=responses.HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=responses.HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/createaccount", response_class=responses.HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("createaccount.html", {"request": request})


@app.get("/dashboard", response_class=responses.HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/explore", response_class=responses.HTMLResponse)
async def explore(request: Request):
    return templates.TemplateResponse("explore.html", {"request": request})


@app.get("/chat", response_class=responses.HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        conn.commit()

        return responses.RedirectResponse("/login", status_code=303)

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


@app.post("/login-validation")
async def login(
    user_email: str = Form(...),
    user_password: str = Form(...)
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT password, is_active FROM users WHERE email=%s",
        (user_email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return responses.RedirectResponse("/", status_code=303)

    if user["is_active"] == 0:
        return "Account is deactivated"

    stored_password = user["password"].encode()

    if bcrypt.checkpw(user_password.encode(), stored_password):
        return responses.RedirectResponse("/dashboard", status_code=302)

    return "Incorrect password"