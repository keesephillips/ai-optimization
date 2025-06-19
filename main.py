import os
import json
import html
import boto3
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import URL

load_dotenv()


REGION = os.getenv("AWS_REGION", "us-east-2")
PROMPT_ARN = os.getenv(
    "BEDROCK_ARN",
    "arn:aws:bedrock:us-east-2:381492212823:prompt/QSG8T98UZM"
)
PROMPT_VAR_NAME = os.getenv("PROMPT_VAR_NAME", "user_input")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "8200E54A64AF2F8FFB509F99AFE8CF4C")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise ValueError(
        "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set in the environment."
    )

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

app = FastAPI(
    title="AI Enterprise Chatbot",
    description="A chatbot interface using AWS Bedrock using FastAPI."
)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
templates = Jinja2Templates(directory="templates")


def render_conversation(turns: list[dict]) -> str:
    """
    Takes a list of conversation turns and renders them as HTML.
    Each turn is a dictionary with 'role' ('user' or 'assistant') and 'text'.
    """
    rows = []
    for t in turns:
        # Determine CSS class and label based on the role
        role_cls = "user" if t["role"] == "user" else "assistant"
        label = "You" if t["role"] == "user" else "Chatbot"
        # Escape user-generated text to prevent XSS attacks
        escaped_text = html.escape(t["text"])
        # Append the formatted HTML for the message
        rows.append(
            f'<div class="msg"><span class="{role_cls}">{label}:</span> {escaped_text}</div>'
        )
    return "\n".join(rows)


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """
    Handles GET requests to the root URL.
    It retrieves the conversation from the session and renders the main chat page.
    """
    # Retrieve conversation history from the session, or start a new one
    conversation_history = request.session.get("conversation", [])
    
    # Render the HTML for the conversation turns
    conversation_html = render_conversation(conversation_history)
    
    # Render the main template, passing in the request context and conversation
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "conversation": conversation_html}
    )


@app.post("/chat", response_class=RedirectResponse)
async def handle_chat_message(request: Request, message: str = Form(...)):
    """
    Handles POST requests from the chat form submission.
    It processes the user's message, gets a response from Bedrock,
    updates the session, and redirects back to the main chat page.
    """
    # Retrieve the current conversation from the session, default to empty list
    conversation = request.session.get("conversation", [])
    
    user_text = message.strip()
    if user_text:
        # Add the user's message to the conversation history
        conversation.append({"role": "user", "text": user_text})
        
        # --- Call Bedrock API ---
        try:
            # Note: The boto3 call is synchronous. For very high-concurrency apps,
            # you might consider running this in a thread pool using Starlette's
            # run_in_threadpool or using an async library like aioboto3.
            response = bedrock.converse(
                modelId=PROMPT_ARN,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_text}]
                    }
                ],
                # If your prompt template uses variables, you can use this instead:
                # promptVariables={PROMPT_VAR_NAME: {"text": user_text}},
            )
            # Extract the assistant's response text
            assistant_text = response["output"]["message"]["content"][0]["text"]
        except Exception as exc:
            # Provide a helpful error message if the API call fails
            print(f"Bedrock API Error: {exc}")
            assistant_text = f"Sorry, I encountered an error: {exc}"
        
        # Add the assistant's response to the conversation history
        conversation.append({"role": "assistant", "text": assistant_text})
        
        # Save the updated conversation back into the session
        request.session["conversation"] = conversation

    # Redirect to the root URL to display the updated chat (PRG Pattern)
    return RedirectResponse(url="/", status_code=303)
