from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

@app.post("/generate")
def generate(prompt: Prompt):
    return {"response": f"Mantu AI: {prompt.text}"}
