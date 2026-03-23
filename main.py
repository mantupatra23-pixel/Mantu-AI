from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import sqlite3
from pydantic import BaseModel
import requests
import os
import json
import shutil
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# ✅ app define
app = FastAPI()

# =========================
# 🌐 STATIC PROJECT SERVE (NEW 🔥)
# =========================

# ✅ test route
@app.get("/api")
def home():
    return {"msg": "Mantu AI Backend Running 🚀"}

# =========================
# 🗄️ DATABASE INIT (NEW 🔥)
# =========================
conn = sqlite3.connect("projects.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    prompt TEXT,
    language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================
# 🤖 GROQ AI CODE GENERATOR
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_code(prompt, tech):

    if tech == "flutter":
        instruction = """
Create Flutter app.

Return ONLY JSON:
{
 "lib/main.dart": "full flutter code"
}
"""

    elif tech == "node":
        instruction = """
Create Node.js Express API.

Return ONLY JSON:
{
 "server.js": "express server code",
 "package.json": "dependencies"
}
"""

    else:
        instruction = """
Create modern website.

Return ONLY JSON:
{
 "index.html": "homepage",
 "about.html": "about page",
 "style.css": "design"
}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"{instruction}\n\nProject idea: {prompt}"
            }
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json()

    return result["choices"][0]["message"]["content"]


# =========================
# 🚀 FULL STACK GENERATOR (ULTRA 🔥)
# =========================
def generate_fullstack(prompt):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",  # ✅ FIXED ERROR
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"""
Create FULL STACK APP for: {prompt}

Return ONLY JSON:
{{
 "frontend/index.html": "...",
 "frontend/style.css": "...",
 "backend/app.js": "...",
 "backend/routes.js": "...",
 "database/data.json": "..."
}}
"""
            }
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json()

    return result["choices"][0]["message"]["content"]

# =========================
# 🔐 ENV LOAD
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")


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
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def landing():
    return open("landing.html").read()

@app.get("/start", response_class=HTMLResponse)
def start_page():
    return open("start.html").read()

@app.get("/builder", response_class=HTMLResponse)
def builder():
    return open("builder.html").read()

@app.get("/app", response_class=HTMLResponse)
def app_page():
    return open("index.html").read()

# =========================
# 🧠 TECH DETECTOR (NEW 🔥)
# =========================
def detect_tech(prompt):
    text = prompt.lower()

    if "mobile" in text or "android" in text:
        return "flutter"
    elif "api" in text or "backend" in text:
        return "node"
    else:
        return "next"

# =========================
# 🧠 CREATE PROJECT (AI GENERATOR 🔥)
# =========================
def create_project(name, prompt):

    base_path = f"projects/{name}"
    os.makedirs(base_path, exist_ok=True)

    # 🔥 detect tech
    tech = detect_tech(prompt)

    try:
        # 🤖 AI generate
        raw = generate_code(prompt, tech)

        try:
            # 🧠 MULTI FILE JSON
            files = json.loads(raw)

            for filename, content in files.items():
                file_path = os.path.join(base_path, filename)

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, "w") as f:
                    f.write(content)

            return tech  # 🔥 important (chat me use hoga)

        except:
            # ⚠️ single file fallback

            if tech == "flutter":
                file = "lib/main.dart"
            elif tech == "node":
                file = "server.js"
            else:
                file = "index.html"

            with open(os.path.join(base_path, file), "w") as f:
                f.write(raw)

            return tech

    except Exception:
        # 🧠 OFFLINE FALLBACK

        html_code = f"""
<!DOCTYPE html>
<html>
<head>
<title>{name}</title>
<style>
body {{
  background:#0f172a;
  color:white;
  text-align:center;
  padding:40px;
  font-family:sans-serif;
}}
</style>
</head>
<body>

<h1>🚀 {name}</h1>
<p>{prompt}</p>

</body>
</html>
"""

        with open(f"{base_path}/index.html", "w") as f:
            f.write(html_code)

        return "html"


# =========================
# 🚀 FULL STACK PROJECT (ULTRA 🔥)
# =========================
def create_fullstack_project(name, prompt):

    base_path = f"projects/{name}"
    os.makedirs(base_path, exist_ok=True)

    try:
        raw = generate_fullstack(prompt)

        try:
            files = json.loads(raw)

            for path, content in files.items():
                full_path = os.path.join(base_path, path)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, "w") as f:
                    f.write(content)

            return "fullstack"

        except:
            return "AI error (invalid JSON)"

    except Exception:
        return "AI error (request failed)"


# =========================
# 🌍 RENDER URL
# =========================
def get_render_url(project):
    return f"https://{project}.onrender.com"

# =========================
# ⚙️ BACKEND RUNNER (NEW 🔥)
# =========================
import subprocess

def start_backend(project):
    path = f"projects/{project}/backend"

    try:
        subprocess.Popen(
            ["node", "app.js"],
            cwd=path
        )
        return "Backend started"
    except:
        return "Backend error"

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
def ai_generate(prompt, system_prompt=""):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# 🚀 DOCKER DEPLOY (NEW 🔥)
# =========================
import random
import subprocess

def deploy_project(name):
    port = random.randint(9000, 9999)

    path = f"/home/ubuntu/Mantu-AI/projects/{name}"

    subprocess.Popen([
        "docker", "run", "-d",
        "-p", f"{port}:8000",
        path
    ])

    return f"http://54.224.241.169:{port}"


# =========================
# 🐍 PYTHON CODE GENERATOR (NEW 🔥)
# =========================
@app.post("/generate/python")
async def generate_python(prompt: str):
    system_prompt = """
You are a Python expert.
Generate clean production-ready Python code.
Only return code.
"""
    result = ai_generate(prompt, system_prompt)
    return {"code": result}

# =========================
# ▶️ RUN PYTHON CODE (NEW 🔥)
# =========================
import subprocess
import uuid

@app.post("/run/python")
async def run_python(code: str):
    filename = f"/tmp/{uuid.uuid4().hex}.py"

    with open(filename, "w") as f:
        f.write(code)

    try:
        result = subprocess.run(
            ["python3", filename],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}

# =========================
# 🧠 MULTI CODE GENERATOR (NEW 🔥)
# =========================
@app.post("/generate/code")
async def generate_code(data: dict):
    prompt = data.get("prompt", "")
    lang = data.get("lang", "")

    system_map = {
        "html": "Create clean modern HTML CSS UI",
        "python": "Write Python code",
        "node": "Write Node.js backend",
        "flutter": "Create Flutter UI",
        "fullstack": "Create full stack app"
    }

    system_prompt = system_map.get(lang, "")

    result = ai_generate(prompt, system_prompt)

    return {"code": result}

# =========================
# 🛠 DEBUG / FIX CODE (NEW 🔥)
# =========================
@app.post("/debug")
async def debug_code(data: dict):
    code = data.get("code")

    system_prompt = """
Fix this code.
Return ONLY corrected code.
No explanation.
"""

    result = ai_generate(code, system_prompt)

    return {"fixed": result}

# =========================
# 👨‍💻 DEV CHAT (CODE MODIFY 🔥)
# =========================
@app.post("/dev-chat")
async def dev_chat(data: dict):
    prompt = data.get("prompt")
    code = data.get("code")

    system_prompt = f"""
You are a senior developer.

User request:
{prompt}

Existing code:
{code}

Modify the code accordingly.
Return only updated code.
"""

    result = ai_generate(prompt, system_prompt)

    return {"updated_code": result}

# =========================
# 👁️ PREVIEW API (NEW 🔥)
# =========================
class Code(BaseModel):
    html: str

@app.post("/preview")
def preview(code: Code):
    return {"html": code.html}

# =========================
# 💾 SAVE PROJECT (DB 🔥)
# =========================
@app.post("/save-project")
def save_project(data: dict):
    name = data.get("name")
    prompt = data.get("prompt")
    language = data.get("language")

    cursor.execute(
        "INSERT INTO projects (name, prompt, language) VALUES (?, ?, ?)",
        (name, prompt, language)
    )
    conn.commit()

    return {"msg": "saved"}

# =========================
# 📊 GET PROJECTS LIST (NEW 🔥)
# =========================
@app.get("/projects")
def get_projects():
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    rows = cursor.fetchall()

    projects = []
    for r in rows:
        projects.append({
            "id": r[0],
            "name": r[1],
            "prompt": r[2],
            "language": r[3]
        })

    return {"projects": projects}

# =========================
# 🤖 SMART CHAT (FINAL 🔥)
# =========================
@app.post("/chat")
async def chat(prompt: Prompt):
    text = prompt.text.lower()

    # 🚀 DEPLOY DIRECT MODE (TOP PRIORITY 🔥)
    if ("deploy" in text and ("app" in text or "website" in text)) or ("app" in text and "deploy" in text):
        project_name = text.replace(" ", "-")

        # create project
        create_fullstack_project(project_name, text)

        # 🔥 SAVE TO DB
        save_project({
        "name": project_name,
        "prompt": text,
        "language": "fullstack"
       })

        # deploy
        url = deploy_project(project_name)

        ai_response = f"""
🚀 APP DEPLOYED!

📁 Project: {project_name}

🌐 Live URL:
{url}
"""

    # 🚀 FULL STACK MODE
    elif "full" in text or "api" in text:
        project_name = text.replace(" ", "-")

        create_fullstack_project(project_name, text)

        # backend run
        status = start_backend(project_name)

        url = f"/apps/{project_name}/frontend/index.html"

        ai_response = f"""
🚀 FULL STACK APP LIVE!

📁 Project: {project_name}

🌐 Frontend:
http://localhost:8000{url}

⚙️ {status}
"""

    # 🔥 NORMAL AI APP
    elif "app" in text or "website" in text:
        project_name = text.replace(" ", "-")

        tech = create_project(project_name, text)

        url = f"/apps/{project_name}/index.html"

        ai_response = f"""
🚀 {tech.upper()} Project Created!

📁 Folder: {project_name}

🌐 Open:
http://localhost:8000{url}
"""

    # 🤖 DEFAULT
    else:
        ai_response = "🤖 AI: Processing..."

    # 🧠 MEMORY SAVE
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
# 🌍 PROJECT PREVIEW (LIVE)
# =========================
from fastapi.responses import FileResponse
import os

@app.get("/project/{name}")
def run_project(name: str):
    path = f"{name}/index.html"   # ⚠️ important fix

    if os.path.exists(path):
        return FileResponse(path)

    return {"error": "Project not found"}

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
# 📦 DOWNLOAD PROJECT ZIP (NEW 🔥)
# =========================
import os
import zipfile
from fastapi.responses import FileResponse

@app.get("/download/{name}")
def download_project(name: str):
    folder = f"projects/{name}"
    zip_path = f"{folder}.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path, os.path.relpath(full_path, folder))

    return FileResponse(zip_path, filename=f"{name}.zip")

# =========================
# 🎨 TEMPLATE API
# =========================
@app.post("/template")
async def template_api(prompt: Prompt):
    return {"html": templates.get(prompt.text.lower(), "<h1>Custom App</h1>")}
