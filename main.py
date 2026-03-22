from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# ENV load
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# Request model
class Prompt(BaseModel):
    text: str

# Home route (frontend load)
@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

# AI Generate route
@app.post("/generate")
def generate(prompt: Prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are Mantu AI, a smart assistant."},
            {"role": "user", "content": prompt.text}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()

        return {
            "response": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}"
        }
