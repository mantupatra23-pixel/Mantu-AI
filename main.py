from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import requests
import os
import shutil
from dotenv import load_dotenv

# =========================
# 🔐 ENV LOAD
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

app = FastAPI()

# =========================
# 📦 MODEL
# =========================
class Prompt(BaseModel):
    text: str

# =========================
# 🧠 MEMORY
# =========================
chat_history = []
deploy_logs = []

# =========================
# 🎨 TEMPLATE SYSTEM
# =========================
templates = {
    "blog": "<h1>📝 Blog App</h1>",
    "todo": "<h1>✅ Todo App</h1>",
    "ai": "<h1>🤖 AI App</h1>"
}

# =========================
# 🌐 FRONTEND ROUTES
# =========================
@app.get("/", response_class=HTMLResponse)
def landing():
    return open("landing.html").read()

@app.get("/app", response_class=HTMLResponse)
def app_page():
    return open("index.html").read()

@app.get("/builder", response_class=HTMLResponse)
def builder():
    return open("builder.html").read()

@app.get("/start.html", response_class=HTMLResponse)
def start_page():
    return open("start.html").read

# =========================
# 🧠 CREATE PROJECT
# =========================
def create_project(name):
    os.makedirs(name, exist_ok=True)

    with open(f"{name}/main.py", "w") as f:
        f.write("""
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"msg":"Hello from Mantu AI 🚀"}
""")

    with open(f"{name}/index.html", "w") as f:
        f.write(f"<h1>{name} App 🚀</h1>")

    return f"✅ Project '{name}' created"

# =========================
# 🌍 RENDER URL
# =========================
def get_render_url(project):
    return f"https://{project}.onrender.com"

# =========================
# 🚀 GITHUB FUNCTIONS
# =========================
def create_github_repo(name):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": name}
    requests.post(url, headers=headers, json=data)

def push_code(project):
    os.system(f"cd {project} && git init")
    os.system(f"cd {project} && git add .")
    os.system(f"cd {project} && git commit -m 'init'")
    os.system(f"cd {project} && git branch -M main")
    os.system(f"cd {project} && git remote add origin https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{project}.git")
    os.system(f"cd {project} && git push -u origin main")

# =========================
# 🤖 AI GENERATE (GROQ)
# =========================
@app.post("/generate")
async def generate(prompt: Prompt):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        messages = [{"role": "system", "content": "You are Mantu AI"}]

        for msg in chat_history[-5:]:
            if "user" in msg:
                messages.append({"role": "user", "content": msg["user"]})
            if "ai" in msg:
                messages.append({"role": "assistant", "content": msg["ai"]})

        messages.append({"role": "user", "content": prompt.text})

        res = requests.post(url, headers=headers, json={
            "model": "llama3-70b-8192",
            "messages": messages
        })

        reply = res.json()["choices"][0]["message"]["content"]

        chat_history.append({"user": prompt.text})
        chat_history.append({"ai": reply})

        return {"response": reply}

    except Exception as e:
        return {"response": str(e)}

# =========================
# 🤖 SMART CHAT (FINAL 🔥)
# =========================
@app.post("/chat")
async def chat(prompt: Prompt):
    text = prompt.text.lower()

    if "app" in text:
        project_name = text.replace(" ", "-")

        # 1. create project
        create_project(project_name)

        # 2. create repo
        create_github_repo(project_name)

        # 3. push code
        push_code(project_name)

        # 4. expected live url
        live_url = get_render_url(project_name)

        ai_response = f"""
🚀 Project Created & Deploy Started!

📦 Repo:
https://github.com/{GITHUB_USERNAME}/{project_name}

🌐 Live URL (after deploy):
{live_url}
"""

    elif "deploy" in text:
        ai_response = "☁️ Deploy Agent starting..."

    else:
        ai_response = "🤖 AI: Processing..."

    chat_history.append({"user": prompt.text})
    chat_history.append({"ai": ai_response})

    return {
        "response": ai_response,
        "history": chat_history
    }

# =========================
# 📦 DOWNLOAD ZIP
# =========================
@app.get("/download/{name}")
def download(name: str):
    zip_file = shutil.make_archive(name, 'zip', name)
    return FileResponse(zip_file, filename=f"{name}.zip")

# =========================
# 🌐 AUTO DEPLOY
# =========================
@app.post("/auto-deploy")
async def auto_deploy(prompt: Prompt):
    name = prompt.text.strip().replace(" ", "-")

    create_project(name)

    url = get_render_url(name)

    deploy_logs.append({
        "project": name,
        "status": "deploying",
        "url": url
    })

    return {
        "msg": "🚀 Deploy started",
        "url": url
    }

# =========================
# 📊 DEPLOY LOGS
# =========================
@app.get("/deploy-logs")
def logs():
    return {"logs": deploy_logs}

# =========================
# 🎨 TEMPLATE API
# =========================
@app.post("/template")
async def template_api(prompt: Prompt):
    return {"html": templates.get(prompt.text.lower(), "<h1>Custom App</h1>")}
