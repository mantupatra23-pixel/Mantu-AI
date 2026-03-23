from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import sqlite3
from pydantic import BaseModel
import requests
import os
import os, json
import json
import shutil
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import zipfile
from fastapi.responses import FileResponse


# ✅ app define
app = FastAPI()

# =========================
# 🌐 STATIC PROJECT SERVE (NEW 🔥)
# =========================
# 🔥 IMPORTANT FIX
PROJECTS_DIR = "projects"
os.makedirs(PROJECTS_DIR, exist_ok=True)

ENV_FILE = "env_store.json" 

app.mount("/apps", StaticFiles(directory="projects"), name="apps")

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
        "model": "mixtral-8x7b-32768",
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
@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

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
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": system_prompt + """
Return response STRICTLY in JSON format:

{
  "files": {
    "index.html": "...",
    "style.css": "...",
    "script.js": "..."
  }
}
"""
            },
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json()

    if "choices" not in result:
        return result

    text = result["choices"][0]["message"]["content"]

    try:
        return eval(text)
    except:
        return {"files": {"index.html": text}}




import base64

@app.post("/deploy/github")
async def deploy_github(data: dict):

    name = data.get("name", "mantu-app")
    files = data.get("files", {})

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 🔥 CREATE REPO
    requests.post(
        "https://api.github.com/user/repos",
        json={"name": name},
        headers=headers
    )

    # 🔥 LOAD ENV (IMPORTANT 🔥)
    env_path = f"projects/{name}/.env"

    if os.path.exists(env_path):
        with open(env_path) as f:
            env_content = f.read()
            files[".env"] = env_content   # 🔥 ADD ENV TO FILES

    # 🔥 PUSH FILES
    for fname, content in files.items():

        url = f"https://api.github.com/repos/{USERNAME}/{name}/contents/{fname}"

        encoded = base64.b64encode(content.encode()).decode()

        requests.put(url,
            json={
                "message": "init commit",
                "content": encoded
            },
            headers=headers
        )

    return {
        "status": "github done",
        "repo": f"https://github.com/{USERNAME}/{name}"
    }

@app.get("/deploy/vercel")
async def deploy_vercel(name: str):

    return {
        "url": f"https://vercel.com/new/clone?repository-url=https://github.com/{USERNAME}/{name}"
    }

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
# 🔐 ENV SAVE SYSTEM
# =========================

@app.post("/save_env")
async def save_env(data: dict):
    name = data.get("project")
    envs = data.get("env", {})

    try:
        with open(ENV_FILE, "r") as f:
            all_env = json.load(f)
    except:
        all_env = {}

    all_env[name] = envs

    with open(ENV_FILE, "w") as f:
        json.dump(all_env, f, indent=2)

    return {"status": "saved"}

# 🔥 CREATE .env FILE INSIDE PROJECT
    import os

    project_path = f"projects/{name}"
    os.makedirs(project_path, exist_ok=True)

    env_path = f"{project_path}/.env"

    with open(env_path, "w") as f:
        for k,v in envs.items():
            f.write(f"{k}={v}\n")

# =========================
# 📥 GET ENV (ADD HERE 🔥)
# =========================
@app.get("/get_env/{name}")
async def get_env(name: str):
    try:
        with open(ENV_FILE) as f:
            data = json.load(f)
        return data.get(name, {})
    except:
        return {}

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
# 🚀 GENERATE MULTI FILE (ADD HERE 🔥)
# =========================
@app.post("/generate/files")
async def generate_files(data: dict):
    prompt = data.get("prompt")

    system_prompt = """
Generate a full web project.

Return JSON like:
{
 "files": {
   "index.html": "...",
   "style.css": "...",
   "script.js": "..."
 }
}
Only return JSON.
"""

    result = ai_generate(prompt, system_prompt)

    import json
    try:
        parsed = json.loads(result)
    except:
        parsed = {"files": {"index.html": result}}

    return parsed

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
# 🚀 DEPLOY (ADD HERE 🔥)
# =========================
@app.post("/deploy")
async def deploy(data: dict):

    name = data.get("name", "app")

    path = f"projects/{name}"
    os.makedirs(path, exist_ok=True)

    files = data.get("files", {})

    for filename, content in files.items():
        file_path = os.path.join(path, filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            f.write(content)

    url = f"/apps/{name}/index.html"

    return {"url": url}

# =========================
# 📦 EXPORT ZIP (ADD HERE 🔥)
# =========================
import zipfile
from fastapi.responses import FileResponse

@app.post("/export_zip")
async def export_zip(data: dict):
    name = data.get("name", "project")
    files = data.get("files", {})

    zip_path = f"{name}.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for fname, content in files.items():
            zipf.writestr(fname, content)

    return FileResponse(zip_path, filename=zip_path)

# =========================
# 💾 SAVE PROJECT (ADD HERE 🔥)
# =========================
@app.post("/save_project")
async def save_project(data: dict):
    name = data.get("name", "project")
    files = data.get("files", {})

    path = os.path.join(PROJECTS_DIR, name)
    os.makedirs(path, exist_ok=True)

    for fname, content in files.items():
        file_path = os.path.join(path, fname)

        with open(file_path, "w") as f:
            f.write(content)

    return {"status": "saved", "project": name}

# =========================
# 📂 LOAD PROJECT (ADD HERE 🔥)
# =========================
@app.get("/load_project/{name}")
async def load_project(name: str):
    path = os.path.join(PROJECTS_DIR, name)

    files = {}

    for root, _, filenames in os.walk(path):
        for file in filenames:
            full_path = os.path.join(root, file)
            with open(full_path, "r") as f:
                files[file] = f.read()

    return {"files": files}

# =========================
# 📁 LIST PROJECTS (ADD HERE 🔥)
# =========================
@app.get("/projects")
async def list_projects():
    return {"projects": os.listdir(PROJECTS_DIR)}

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
