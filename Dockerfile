FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```

**Save it.**

---

### 3.3 Create `.dockerignore`

Create a new file called `.dockerignore`

Add this content:
```
__pycache__
*.pyc
.env
.git
.gitignore
venv/
*.db
auth.db
```

**Save it.**

---

## Your Project Should Now Look Like:
```
login/
├── app.py
├── requirements.txt
├── fly.toml              ← NEW
├── Dockerfile            ← NEW
├── .dockerignore         ← NEW
├── .env
├── templates/
│   ├── base.html
│   ├── login.html
│   └── ...
└── venv/