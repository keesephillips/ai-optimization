from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login")
async def login():
    return HTMLResponse("<h1>Login Page</h1><p>Redirect worked!</p>")

@app.get("/test")
async def test():
    return {"message": "API is working"}