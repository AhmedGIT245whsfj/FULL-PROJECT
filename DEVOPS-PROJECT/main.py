import os
import socket

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "CHANGE_ME_TO_A_RANDOM_SECRET"  # غيّرها قبل أي نشر

# Users (demo) - later ممكن تستبدلها ب DB
USERS = {
    "admin": {"password": "admin123", "role": "sysadmin"},
    "dev": {"password": "dev123", "role": "developer"},
    "ops": {"password": "ops123", "role": "devops"},
}

# Role -> image + roadmap (matching your actual image names)
ROLE_DATA = {
    "sysadmin": {
        "title": "System Admin",
        "image_path": "images/systemadmin.jpeg",
        "roadmap": [
            "Linux fundamentals",
            "Users, groups, permissions",
            "Networking basics (IP, DNS, SSH)",
            "System services & logs",
            "Monitoring & backup basics",
        ],
    },
    "developer": {
        "title": "Developer",
        "image_path": "images/web.png",
        "roadmap": [
            "HTML / CSS / JavaScript fundamentals",
            "Python basics",
            "Flask basics (routes, templates)",
            "Git & GitHub workflow",
            "Build small projects & practice",
        ],
    },
    "devops": {
        "title": "DevOps",
        "image_path": "images/devops.png",
        "roadmap": [
            "Linux & networking refresh",
            "Docker fundamentals",
            "Docker Compose basics",
            "CI/CD fundamentals",
            "Terraform basics + deploy a simple app",
        ],
    },
}


def is_logged_in() -> bool:
    return "username" in session and "role" in session


def get_hostname() -> str:
    return os.environ.get("HOSTNAME") or socket.gethostname()


@app.get("/")
def home():
    # لو داخل بالفعل يروح داشبورد
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.get("/login")
def login():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.post("/login")
def login_post():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    user = USERS.get(username)
    if not user or user["password"] != password:
        return render_template("login.html", error="Invalid username or password")

    session["username"] = username
    session["role"] = user["role"]
    return redirect(url_for("dashboard"))


@app.get("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    role = session.get("role")
    data = ROLE_DATA.get(role)

    # Safety fallback لو role غلط
    if not data:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        role=role,
        role_title=data["title"],
        image_path=data["image_path"],
        roadmap=data["roadmap"],
        hostname=get_hostname(),
    )


@app.get("/health")
def health():
    return {"status": "ok", "hostname": get_hostname()}, 200


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    # dev mode
    app.run(host="0.0.0.0", port=5000, debug=True)
