# Quick Start Guide

Get your Flask Auth App running in 5 minutes!

## 1️⃣ Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Run the App

```bash
python app.py
```

Visit: **http://localhost:5000** 🎉

## 4️⃣ Test It Out

1. Click **"Register"** to create an account
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`

2. Click **"Login"** and enter your credentials
3. View your **Dashboard** (protected page!)
4. Check your **Profile**
5. Click **"Logout"**

## 📋 What's Included

✅ **User Registration** with validation
✅ **Secure Login** with password hashing
✅ **Protected Pages** (dashboard, profile)
✅ **SQLite Database** (auto-created)
✅ **Beautiful Bootstrap UI**
✅ **Session Management**

## 🚀 Next: Add OAuth

When you're ready to add Google, Microsoft, or GitHub login:

1. Read `OAUTH_GUIDE.md` for detailed instructions
2. Choose which provider to start with
3. I'll provide complete implementation code

## 🐛 Troubleshooting

**"Port 5000 already in use?"**
```bash
python app.py --port 5001
```

**"Database errors?"**
```bash
rm auth.db
python app.py
```

**"Dependencies not found?"**
```bash
# Make sure venv is activated, then:
pip install -r requirements.txt
```

## 📝 Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with routes |
| `requirements.txt` | Python package dependencies |
| `README.md` | Full documentation |
| `OAUTH_GUIDE.md` | OAuth setup instructions |
| `templates/` | HTML templates for pages |
| `auth.db` | SQLite database (auto-created) |

## 💡 Key Features

### Authentication Methods
- Standard login/registration (✅ Working)
- Google OAuth (🔄 Coming)
- Microsoft OAuth (🔄 Coming)
- GitHub OAuth (🔄 Coming)

### User Data Stored
- Username and email
- Hashed password
- Account creation date
- OAuth provider IDs (for future use)

### Routes
```
GET  /                    → Home page
GET  /register           → Registration form
POST /register           → Create new account
GET  /login              → Login form
POST /login              → Authenticate user
GET  /dashboard          → User dashboard (protected)
GET  /profile            → User profile (protected)
GET  /logout             → End session
```

## 🔒 Security Notes

- Passwords are hashed with Werkzeug (industry standard)
- Sessions are server-side secure
- Input validation on all forms
- Database is SQLite (fine for dev, use PostgreSQL for production)

## 📚 Want to Learn More?

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **OAuth 2.0**: https://oauth.net/2/

---

**Ready?** Start the app and begin testing! 🎯

When you want to add OAuth providers, just ask which one you'd like to tackle first! 🚀