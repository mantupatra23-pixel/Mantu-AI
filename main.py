from fastapi import FastAPI
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
projects = []
deploy_logs = []

# =========================
# 🎨 TEMPLATE SYSTEM
# =========================
templates = {
    "blog": "<h1>📝 Blog App</h1><p>Start writing posts</p>",
    "todo": "<h1>✅ Todo App</h1><p>Manage tasks easily</p>",
    "ai": "<h1>🤖 AI App</h1><p>Build AI tools</p>"
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

@app.get("/start.html", response_class=HTMLResponse)
def start_page():
    return open("start.html").read()

@app.get("/builder.html", response_class=HTMLResponse)
def builder():
    return open("builder.html").read()

# =========================
# 🧠 CREATE PROJECT FUNCTION
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
# 🤖 AI CHAT (GROQ)
# =========================
@app.post("/generate")
def generate(prompt: Prompt):
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
# 🤖 SMART AGENT CHAT
# =========================
@app.post("/chat")
def chat(prompt: Prompt):
    text = prompt.text.lower()

    # 🔥 AUTO PROJECT BUILD
    if "app" in text:
        name = text.replace(" ", "-")
        result = create_project(name)
        ai_response = f"🚀 Code Agent: {result}"

    elif "deploy" in text:
        ai_response = "☁️ Deploy Agent: Deployment starting..."

    elif "error" in text:
        ai_response = "🛠 Fix Agent: Fixing error..."

    elif "money" in text or "earn" in text:
        ai_response = "💰 Business Agent: Monetization system added..."

    else:
        ai_response = "🤖 AI: Processing..."

    chat_history.append({"user": prompt.text})
    chat_history.append({"ai": ai_response})

    return {
        "response": ai_response,
        "history": chat_history
    }

# =========================
# 🚀 CREATE PROJECT (API)
# =========================
@app.post("/create-project")
def create_project_api(prompt: Prompt):
    name = prompt.text.strip().replace(" ", "-")
    msg = create_project(name)
    return {"msg": msg}

# =========================
# 📦 DOWNLOAD ZIP
# =========================
@app.get("/download/{name}")
def download(name: str):
    zip_file = shutil.make_archive(name, 'zip', name)
    return FileResponse(zip_file, filename=f"{name}.zip")

# =========================
# 🚀 FULL BUILD (GITHUB PUSH)
# =========================
@app.post("/full-build")
def full_build(prompt: Prompt):
    name = prompt.text.strip().replace(" ", "-")

    create_project(name)

    # create repo
    requests.post(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
        json={"name": name}
    )

    # push
    os.system(f"cd {name} && git init")
    os.system(f"cd {name} && git add .")
    os.system(f"cd {name} && git commit -m 'init'")
    os.system(f"cd {name} && git branch -M main")
    os.system(f"cd {name} && git remote add origin https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{name}.git")
    os.system(f"cd {name} && git push -u origin main")

    return {"msg": "🚀 Pushed to GitHub", "repo": f"https://github.com/{GITHUB_USERNAME}/{name}"}

# =========================
# 🌐 AUTO DEPLOY
# =========================
@app.post("/auto-deploy")
def auto_deploy(prompt: Prompt):
    name = prompt.text.strip().replace(" ", "-")

    create_project(name)

    deploy_logs.append({
        "project": name,
        "status": "deploying..."
    })

    return {"msg": "🚀 Deploy Started", "project": name}

# =========================
# 🧱 FULL PROJECT GENERATOR
# =========================
@app.post("/generate-full-project")
def generate_full_project(prompt: Prompt):
    name = prompt.text.strip().replace(" ", "-")

    os.makedirs(f"{name}/backend", exist_ok=True)
    os.makedirs(f"{name}/frontend", exist_ok=True)

    with open(f"{name}/backend/main.py", "w") as f:
        f.write("print('Backend Ready')")

    with open(f"{name}/frontend/index.html", "w") as f:
        f.write(f"<h1>{name} Frontend 🚀</h1>")

    return {"msg": "🔥 Full Project Generated", "project": name}

# =========================
# 🎨 TEMPLATE API
# =========================
@app.post("/template")
def template_api(prompt: Prompt):
    return {"html": templates.get(prompt.text.lower(), "<h1>Custom App</h1>")}

# =========================
# 📊 DEPLOY TRACKING
# =========================
@app.get("/deploy-logs")
def logs():
    return {"logs": deploy_logs}
