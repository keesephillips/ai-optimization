import os
import json
import html
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="NENRRFJEN81324BFQWJ23")
templates = Jinja2Templates(directory="app/templates")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "user" and password == "password":
        request.session["user"] = username
        request.session["conversation"] = []  
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    request.session["user"] = username
    request.session["conversation"] = []
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/")
async def chat_page(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
    
    conversation = request.session.get("conversation", [])
    html_conv = ""
    for msg in conversation:
        role = "You" if msg["role"] == "user" else "Assistant"
        html_conv += f'<div><b>{role}:</b> {html.escape(msg["text"])}</div><br>'
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "conversation": html_conv, 
        "user": request.session.get("user")
    })

@app.post("/chat")
async def chat(request: Request, message: str = Form(...)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
    
    conversation = request.session.get("conversation", [])
    conversation.append({"role": "user", "text": message})
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": "You are a helpful AI assistant. Always provide direct, helpful responses. Never say you encountered an error processing a message unless there is a genuine technical issue. Answer all questions to the best of your ability.",
        "messages": [{"role": "user", "content": message}]
    })
    
    try:
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        assistant_text = response_body.get('content', [{}])[0].get('text', '')
        
    except Exception as e:
        assistant_text = f"Error: {str(e)}"
    
    conversation.append({"role": "assistant", "text": assistant_text})
    request.session["conversation"] = conversation
    
    return RedirectResponse(url="/", status_code=303)