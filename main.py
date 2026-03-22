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
# 🤖 AGENT ROUTER (SMART AI)
# =========================
def agent_router(text):
    text = text.lower()

    if "app" in text:
        return "🚀 Code Agent: Building your app..."
    elif "deploy" in text:
        return "☁️ Deploy Agent: Deploying your project..."
    elif "error" in text:
        return "🛠 Fix Agent: Fixing errors..."
    elif "money" in text or "earn" in text:
        return "💰 Business Agent: Adding earning system..."
    else:
        return "🤖 AI: Processing..."

# =========================
# 🌐 FRONTEND ROUTES
# =========================
@app.get("/", response_class=HTMLResponse)
def landing():
    return open("landing.html").read()

@app.get("/app", response_class=HTMLResponse)
def app_page():
    return open("index.html").read()

@app.get("/", response_class=HTMLResponse)
def entry():
    return open("start.html").read()


# =========================
# 🤖 AI CHAT (GROQ + MEMORY)
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
        return {"response": f"Error: {str(e)}"}

# =========================
# 💬 SMART CHAT (AGENT + MEMORY)
# =========================
@app.post("/chat")
def chat(prompt: Prompt):
    user_msg = prompt.text

    ai_response = agent_router(user_msg)

    chat_history.append({"user": user_msg})
    chat_history.append({"ai": ai_response})

    return {
        "response": ai_response,
        "history": chat_history
    }

# =========================
# 🚀 CREATE PROJECT
# =========================
@app.post("/create-project")
def create_project(prompt: Prompt):
    try:
        project = prompt.text.strip().replace(" ", "-")
        os.makedirs(project, exist_ok=True)

        with open(f"{project}/app.py", "w") as f:
            f.write(f"""from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {{"msg": "Welcome to {prompt.text}"}}
""")

        with open(f"{project}/index.html", "w") as f:
            f.write(f"<h1>{prompt.text}</h1><p>Ready 🚀</p>")

        push_to_git(project)

        return {"msg": f"✅ {project} created"}

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 💾 SAVE PROJECT
# =========================
@app.post("/save-project")
def save_project(prompt: Prompt):
    projects.append(prompt.text)
    return {"projects": projects}

# =========================
# 📦 DOWNLOAD ZIP
# =========================
@app.get("/download/{name}")
def download(name: str):
    try:
        zip_file = shutil.make_archive(name, 'zip', name)
        return FileResponse(zip_file, filename=f"{name}.zip")
    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 🔧 LOCAL GIT
# =========================
def push_to_git(project):
    try:
        os.system(f"cd {project} && git init")
        os.system(f"cd {project} && git add .")
        os.system(f"cd {project} && git commit -m 'init'")
    except:
        pass

# =========================
# 🚀 FULL BUILD (GITHUB PUSH)
# =========================
@app.post("/full-build")
def full_build(prompt: Prompt):
    try:
        project = prompt.text.strip().replace(" ", "-")
        os.makedirs(project, exist_ok=True)

        with open(f"{project}/app.py", "w") as f:
            f.write(f"# AI generated app for {prompt.text}")

        with open(f"{project}/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\n")

        requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {GITHUB_TOKEN}"},
            json={"name": project}
        )

        os.system(f"cd {project} && git init")
        os.system(f"cd {project} && git add .")
        os.system(f"cd {project} && git commit -m 'init'")
        os.system(f"cd {project} && git branch -M main")
        os.system(f"cd {project} && git remote add origin https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{project}.git")
        os.system(f"cd {project} && git push -u origin main")

        return {"msg": "🚀 Project Created", "repo": f"https://github.com/{GITHUB_USERNAME}/{project}"}

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 🌐 AUTO DEPLOY
# =========================
@app.post("/auto-deploy")
def auto_deploy(prompt: Prompt):
    try:
        name = prompt.text.strip().replace(" ", "-")
        os.makedirs(name, exist_ok=True)

        with open(f"{name}/main.py", "w") as f:
            f.write("print('Hello from Mantu AI')")

        with open(f"{name}/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\n")

        requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {GITHUB_TOKEN}"},
            json={"name": name}
        )

        os.system(f"cd {name} && git init")
        os.system(f"cd {name} && git add .")
        os.system(f"cd {name} && git commit -m 'init'")
        os.system(f"cd {name} && git branch -M main")
        os.system(f"cd {name} && git remote add origin https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{name}.git")
        os.system(f"cd {name} && git push -u origin main")

        deploy_logs.append({"project": name, "status": "deploying..."})

        return {"msg": "🚀 Deploy Started", "repo": f"https://github.com/{GITHUB_USERNAME}/{name}"}

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 🧱 FULL PROJECT GENERATOR
# =========================
@app.post("/generate-full-project")
def generate_full_project(prompt: Prompt):
    try:
        name = prompt.text.strip().replace(" ", "-")

        os.makedirs(f"{name}/backend", exist_ok=True)
        os.makedirs(f"{name}/frontend", exist_ok=True)

        with open(f"{name}/backend/main.py", "w") as f:
            f.write("""from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"msg":"Hello from backend"}
""")

        with open(f"{name}/frontend/index.html", "w") as f:
            f.write(f"<h1>{prompt.text} App</h1>")

        return {"msg": "🔥 Full Project Generated", "project": name}

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 🎨 TEMPLATE API
# =========================
@app.post("/template")
def use_template(prompt: Prompt):
    return {"html": templates.get(prompt.text.lower(), "<h1>Custom App</h1>")}

# =========================
# 📊 DEPLOY TRACKING
# =========================
@app.post("/track-deploy")
def track(prompt: Prompt):
    deploy_logs.append({"project": prompt.text, "status": "deploying..."})
    return {"logs": deploy_logs}

@app.get("/deploy-logs")
def logs():
    return {"logs": deploy_logs}
