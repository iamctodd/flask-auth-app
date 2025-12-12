# 🔐 Flask Authentication App

A modern, extensible Flask authentication system with standard login/registration and preparation for OAuth providers (Google, Microsoft, GitHub).

## Features

### Phase 1: Core Authentication ✅
- ✅ User registration with validation
- ✅ Secure password hashing (Werkzeug)
- ✅ Standard login system
- ✅ Session management
- ✅ Protected routes with decorators
- ✅ SQLite database with SQLAlchemy
- ✅ Beautiful Bootstrap 5 UI

### Phase 2: OAuth Providers (In Progress)
- ⏳ Google OAuth
- ⏳ Microsoft OAuth
- ⏳ GitHub OAuth
- ⏳ Account linking (connect multiple auth methods)

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── auth.db               # SQLite database (created on first run)
└── templates/
    ├── base.html         # Base template with navbar
    ├── index.html        # Home page
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # User dashboard (protected)
    ├── profile.html      # User profile (protected)
    ├── 404.html          # 404 error page
    └── 500.html          # 500 error page
```

## Setup Instructions

### 1. Clone/Setup the Project
```bash
# Navigate to project directory
cd path/to/flask-auth-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5000`

## Usage

### Create an Account
1. Click "Register" or go to `/register`
2. Enter username, email, and password
3. Click "Create Account"

### Login
1. Click "Login" or go to `/login`
2. Enter your username and password
3. You'll be redirected to your dashboard

### View Profile
- Click "Profile" in the navbar to see your account details
- View connected OAuth providers (coming soon)

## Database Models

### User Model
```python
User:
  - id (Integer, Primary Key)
  - username (String, Unique) - used for login
  - email (String, Unique)
  - password_hash (String) - bcrypt hashed
  - created_at (DateTime)
  
  # OAuth fields (for future use)
  - google_id (String, Unique)
  - microsoft_id (String, Unique)
  - github_id (String, Unique)
```

## Security Features

- **Password Hashing**: Uses Werkzeug's `generate_password_hash()` with salting
- **Session Management**: Secure server-side sessions
- **CSRF Protection**: Ready to add with Flask-WTF
- **Input Validation**: Server-side validation on all forms
- **Password Requirements**: Minimum 6 characters

## Configuration

Edit `app.py` to change:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this'  # IMPORTANT!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
```

### For Production
```bash
export SECRET_KEY='your-production-secret-key'
export FLASK_ENV='production'
```

## Next Steps: Adding OAuth

### Phase 2A: Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials (Web Application)
3. Add authorized redirect URIs: `http://localhost:5000/oauth/google/callback`
4. We'll add Google login button and OAuth flow

### Phase 2B: Microsoft OAuth
1. Go to [Azure Portal](https://portal.azure.com)
2. Register a new application
3. Create Client Secrets
4. Add redirect URI: `http://localhost:5000/oauth/microsoft/callback`
5. We'll add Microsoft login button and OAuth flow

### Phase 2C: GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:5000/oauth/github/callback`
4. We'll add GitHub login button and OAuth flow

We'll implement these step-by-step!

## Troubleshooting

### Database Issues
If you get database errors, delete `auth.db` and restart:
```bash
rm auth.db
python app.py
```

### Port Already in Use
If port 5000 is in use:
```bash
python app.py --port 5001
```

### Import Errors
Make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Testing

Test users can be created via the registration form. Default test account:
- Username: `testuser`
- Password: `password123`

## API Endpoints

| Method | Route | Purpose | Authentication |
|--------|-------|---------|-----------------|
| GET | `/` | Home page | None |
| GET | `/register` | Registration form | None |
| POST | `/register` | Create new account | None |
| GET | `/login` | Login form | None |
| POST | `/login` | Authenticate user | None |
| GET | `/dashboard` | User dashboard | Required |
| GET | `/profile` | User profile | Required |
| GET | `/logout` | End session | Required |

## Performance Optimization

For production, consider:
- Using PostgreSQL instead of SQLite
- Adding Redis for session caching
- Enabling database connection pooling
- Adding rate limiting to login/register endpoints
- Implementing email verification

## Contributing

This is a learning project! Feel free to:
- Add new OAuth providers
- Improve the UI/UX
- Add email verification
- Implement 2FA
- Add password reset functionality

## License

MIT License - Feel free to use this for your projects!

---

**Ready to add OAuth?** Let me know which provider you'd like to add first (Google, Microsoft, or GitHub), and I'll create a step-by-step guide! 🚀