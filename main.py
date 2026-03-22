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
# 📦 MODELS
# =========================
class Prompt(BaseModel):
    text: str

# =========================
# 🧠 MEMORY
# =========================
chat_history = []
projects = []

# =========================
# 🌐 FRONTEND
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

# =========================
# 🤖 AI CHAT (GROQ + MEMORY)
# =========================
@app.post("/generate")
def generate(prompt: Prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": "You are Mantu AI"}]

    # last 5 history
    for msg in chat_history[-5:]:
        if "user" in msg:
            messages.append({"role": "user", "content": msg["user"]})
        if "ai" in msg:
            messages.append({"role": "assistant", "content": msg["ai"]})

    messages.append({"role": "user", "content": prompt.text})

    try:
        res = requests.post(url, headers=headers, json={
            "model": "llama3-70b-8192",
            "messages": messages
        })

        result = res.json()
        reply = result["choices"][0]["message"]["content"]

        chat_history.append({"user": prompt.text})
        chat_history.append({"ai": reply})

        return {"response": reply}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}

# =========================
# 💬 SIMPLE CHAT (TEST)
# =========================
@app.post("/chat")
def chat(prompt: Prompt):
    chat_history.append({"user": prompt.text})

    response = f"AI: {prompt.text}"
    chat_history.append({"ai": response})

    return {"response": response, "history": chat_history}

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
# 💾 SAVE PROJECT LIST
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

        return FileResponse(
            path=zip_file,
            filename=f"{name}.zip",
            media_type="application/zip"
        )

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}

# =========================
# 🔧 LOCAL GIT INIT
# =========================
def push_to_git(project):
    try:
        os.system(f"cd {project} && git init")
        os.system(f"cd {project} && git add .")
        os.system(f"cd {project} && git commit -m 'init'")
    except Exception as e:
        print("Git Error:", e)

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

        # create repo
        requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {GITHUB_TOKEN}"},
            json={"name": project}
        )

        # push
        os.system(f"cd {project} && git init")
        os.system(f"cd {project} && git add .")
        os.system(f"cd {project} && git commit -m 'init'")
        os.system(f"cd {project} && git branch -M main")
        os.system(f"cd {project} && git remote add origin https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{project}.git")
        os.system(f"cd {project} && git push -u origin main")

        return {
            "msg": "🚀 Project Created & Pushed",
            "repo": f"https://github.com/{GITHUB_USERNAME}/{project}"
        }

    except Exception as e:
        return {"msg": f"❌ {str(e)}"}
