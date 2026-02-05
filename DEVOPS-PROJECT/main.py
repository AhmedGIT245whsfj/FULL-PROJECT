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

INTERVIEW_PACKS = {
    "sysadmin": {
        "sections": [
            {
                "title": "Linux & OS",
                "questions": [
                    "Explain the difference between hard links and soft links.",
                    "How do you check running processes and resource usage on a Linux server?",
                    "What is systemd and how do you manage services?",
                    "What are /etc/passwd and /etc/shadow used for?",
                    "How do you identify and clean up disk space issues?",
                    "What is an inode and why does it matter?",
                ],
            },
            {
                "title": "Networking",
                "questions": [
                    "Explain TCP vs UDP. When would you choose each?",
                    "How does DNS resolution work and how do you troubleshoot it?",
                    "What is CIDR and how do you calculate subnets?",
                    "How do you check open ports and active connections?",
                    "What is NAT and why is it used?",
                    "How do you trace network routes and latency?",
                ],
            },
            {
                "title": "Security, Ops, and Reliability",
                "questions": [
                    "What are the benefits of SSH key-based auth over passwords?",
                    "How do you apply OS updates safely on production servers?",
                    "Explain log rotation and how to implement it.",
                    "What is least privilege and how do you enforce it?",
                    "How would you design a backup and restore plan?",
                    "What monitoring signals are critical for a Linux host?",
                ],
            },
        ]
    },
    "developer": {
        "sections": [
            {
                "title": "Programming Fundamentals",
                "questions": [
                    "Explain OOP vs functional programming with examples.",
                    "What is Big-O and how do you analyze complexity?",
                    "What is a REST API and which HTTP verbs are common?",
                    "How do you handle exceptions and errors cleanly?",
                    "Explain the difference between unit and integration tests.",
                    "What is the difference between INNER JOIN and LEFT JOIN?",
                ],
            },
            {
                "title": "Python & Flask",
                "questions": [
                    "What is WSGI and how does Flask run on a server?",
                    "Describe Flask’s request lifecycle.",
                    "How do you manage secrets and environment variables?",
                    "How would you structure a medium-size Flask project?",
                    "What’s the difference between sessions and cookies?",
                    "How do you validate user input safely?",
                ],
            },
            {
                "title": "Design & Dev Practices",
                "questions": [
                    "How do you design pagination for an API?",
                    "What is caching and when should you use it?",
                    "Explain git merge vs rebase and when to use each.",
                    "How do you approach code reviews?",
                    "What is CI and how does it improve quality?",
                    "How do you handle concurrency in web apps?",
                ],
            },
        ]
    },
    "devops": {
        "sections": [
            {
                "title": "CI/CD & Delivery",
                "questions": [
                    "What is the difference between CI and CD?",
                    "How do you design a safe rollback strategy?",
                    "Explain blue/green vs canary deployments.",
                    "How do you version and tag Docker images?",
                    "How do you manage secrets in a pipeline?",
                    "How do you triage failed CI/CD runs?",
                ],
            },
            {
                "title": "Containers & Runtime",
                "questions": [
                    "What is the difference between an image and a container?",
                    "What are best practices for writing Dockerfiles?",
                    "How do you reduce Docker image size?",
                    "What is a container health check and why use it?",
                    "How do you debug container networking issues?",
                    "Docker Compose vs Kubernetes: when to choose each?",
                ],
            },
            {
                "title": "Cloud, IaC, and Observability",
                "questions": [
                    "What is Infrastructure as Code and why use it?",
                    "How does Terraform state work and why is locking needed?",
                    "What is drift and how do you detect it?",
                    "ALB vs NLB: what are the key differences?",
                    "What are the three pillars of observability?",
                    "How would you set up auto-scaling safely?",
                ],
            },
        ]
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


@app.get("/interview")
def interview_prep():
    if not is_logged_in():
        return redirect(url_for("login"))

    requested_role = (request.args.get("role") or "").strip()
    role = requested_role if requested_role in INTERVIEW_PACKS else session.get("role")
    pack = INTERVIEW_PACKS.get(role)
    role_data = ROLE_DATA.get(role)

    if not pack or not role_data:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "interview.html",
        username=session.get("username"),
        role=role,
        role_title=role_data["title"],
        sections=pack["sections"],
    )


@app.get("/api/interview")
def interview_api():
    if not is_logged_in():
        return {"error": "unauthorized"}, 401

    requested_role = (request.args.get("role") or "").strip()
    role = requested_role if requested_role in INTERVIEW_PACKS else session.get("role")
    pack = INTERVIEW_PACKS.get(role)
    role_data = ROLE_DATA.get(role)

    if not pack or not role_data:
        return {"error": "unknown role"}, 400

    return {
        "role": role,
        "title": role_data["title"],
        "sections": pack["sections"],
    }, 200


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
