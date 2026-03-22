from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import requests
import os
import json
import shutil
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# =========================
# 🌐 STATIC PROJECT SERVE (NEW 🔥)
# =========================
app.mount("/apps", StaticFiles(directory="projects"), name="apps")

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
# 🎨 TEMPLATE API
# =========================
@app.post("/template")
async def template_api(prompt: Prompt):
    return {"html": templates.get(prompt.text.lower(), "<h1>Custom App</h1>")}
