# Google OAuth Implementation Checklist

When you're ready to add Google login, follow this checklist! 🚀

## Pre-Implementation (5 minutes)

- [ ] Read this entire checklist
- [ ] Gather: Email address for Google account
- [ ] Have the app running locally
- [ ] Have browser ready to access Google Cloud Console

---

## Step 1: Create Google Cloud Project (10 minutes)

### 1.1 Create Project
- [ ] Go to https://console.cloud.google.com/
- [ ] Click "Select a Project" at top
- [ ] Click "NEW PROJECT"
- [ ] Enter project name: `Flask Auth App` (or your preference)
- [ ] Click "CREATE"
- [ ] Wait for creation to complete

### 1.2 Enable OAuth 2.0 API
- [ ] Select your new project (dropdown at top)
- [ ] Go to "APIs & Services" → "Library"
- [ ] Search for "Google+ API"
- [ ] Click on it
- [ ] Click "ENABLE"
- [ ] Wait for it to enable

---

## Step 2: Create OAuth 2.0 Credentials (10 minutes)

### 2.1 Create Consent Screen
- [ ] Go to "APIs & Services" → "OAuth consent screen"
- [ ] Choose "External" (for testing)
- [ ] Click "CREATE"
- [ ] Fill in:
  - [ ] App name: `Flask Auth App`
  - [ ] User support email: your-email@gmail.com
  - [ ] Developer contact: your-email@gmail.com
- [ ] Click "SAVE AND CONTINUE"
- [ ] Scopes page: Click "ADD OR REMOVE SCOPES"
  - [ ] Add: `openid`
  - [ ] Add: `email`
  - [ ] Add: `profile`
  - [ ] Click "UPDATE"
- [ ] Click "SAVE AND CONTINUE"
- [ ] Review page: Click "BACK TO DASHBOARD"

### 2.2 Create OAuth Credentials
- [ ] Go to "APIs & Services" → "Credentials"
- [ ] Click "CREATE CREDENTIALS" → "OAuth client ID"
- [ ] Application type: "Web application"
- [ ] Name: `Flask Auth App`
- [ ] Under "Authorized JavaScript origins":
  - [ ] Add: `http://localhost:5000`
  - [ ] Add: `http://127.0.0.1:5000`
- [ ] Under "Authorized redirect URIs":
  - [ ] Add: `http://localhost:5000/oauth/google/callback`
  - [ ] Add: `http://127.0.0.1:5000/oauth/google/callback`
- [ ] Click "CREATE"
- [ ] **Copy and save your credentials!**
  - [ ] Client ID: `___________________________`
  - [ ] Client Secret: `___________________________`

---

## Step 3: Update Your Flask App (20 minutes)

### 3.1 Install Dependencies
```bash
pip install Flask-Authlib python-dotenv
pip freeze > requirements.txt
```
- [ ] Run above commands
- [ ] Verify no errors

### 3.2 Create .env File
- [ ] Create `.env` file in project root (same directory as app.py)
- [ ] Add these lines:
```
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
```
- [ ] Replace with actual values from Step 2.2
- [ ] **DO NOT commit .env to git!**
- [ ] Verify `.gitignore` includes `.env`

### 3.3 Update app.py
You'll need to modify `app.py` to:

**At the top, add:**
```python
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

# After app = Flask(__name__)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

**Add these new routes:**
```python
@app.route('/oauth/google')
def oauth_google():
    """Redirect to Google OAuth consent page"""
    redirect_uri = url_for('oauth_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/oauth/google/callback')
def oauth_google_callback():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user info from Google', 'danger')
            return redirect(url_for('login'))
        
        email = user_info.get('email')
        google_id = user_info.get('sub')
        username = email.split('@')[0]  # Use part before @ as username
        
        # Check if user exists by google_id
        user = User.query.filter_by(google_id=google_id).first()
        
        if user:
            # User exists, log them in
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        
        # Check if email already registered
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Email exists but different provider - offer linking
            flash('This email is already registered. Please log in first to link accounts.', 'warning')
            return redirect(url_for('login'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            google_id=google_id
        )
        # Note: no password for OAuth users
        
        try:
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash(f'Account created with Google! Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account', 'danger')
            return redirect(url_for('login'))
    
    except Exception as e:
        flash('Google authentication failed', 'danger')
        return redirect(url_for('login'))
```

### 3.4 Update Templates

**In `templates/login.html`, replace the OAuth buttons section with:**
```html
<div class="text-center mt-4">
    <p class="text-white mb-3">Or login with:</p>
    <div class="d-flex gap-2 justify-content-center">
        <a href="{{ url_for('oauth_google') }}" class="btn btn-light">
            <img src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" alt="Google" style="height: 24px;">
            Google
        </a>
        <button class="btn btn-light" disabled title="Coming soon">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/512px-Microsoft_logo.svg.png" alt="Microsoft" style="height: 24px;">
            Microsoft
        </button>
        <button class="btn btn-light" disabled title="Coming soon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            GitHub
        </button>
    </div>
</div>
```

**In `templates/register.html`, add similar Google button (after the form):**
```html
<hr>
<div class="text-center mt-4">
    <p class="text-muted mb-3">Or sign up with:</p>
    <a href="{{ url_for('oauth_google') }}" class="btn btn-outline-primary">
        <img src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" alt="Google" style="height: 20px;">
        Google
    </a>
</div>
```

- [ ] Update app.py with OAuth imports and routes
- [ ] Update login.html with Google button
- [ ] Update register.html with Google button
- [ ] Verify syntax (no Python errors)

---

## Step 4: Test Google OAuth (15 minutes)

### 4.1 Start the App
- [ ] Make sure .env file is created with credentials
- [ ] Run: `python app.py`
- [ ] Check console: no errors?
- [ ] Visit http://localhost:5000

### 4.2 Test Registration via Google
- [ ] Click "Register" 
- [ ] Scroll down and click "Google" button
- [ ] You'll be redirected to Google login
- [ ] Log in with your Google account
- [ ] Click "Continue" on consent screen
- [ ] You should be redirected to dashboard
- [ ] Check dashboard shows your Google email
- [ ] Check database: new user created with google_id?

### 4.3 Test Login via Google
- [ ] Click "Logout"
- [ ] Click "Login"
- [ ] Scroll down and click "Google" button
- [ ] You should be logged in (Gmail already authenticated)
- [ ] Should redirect to dashboard
- [ ] Verify correct user loaded

### 4.4 Test Account Creation
- [ ] Log out
- [ ] Create account via standard registration (different email)
- [ ] Log in with Google with a new Google account
- [ ] Should create separate account
- [ ] Check you can switch between accounts by logging in differently

---

## Step 5: Troubleshooting (if needed)

### Issue: "Redirect URI mismatch"
**Solution:**
- [ ] Check your `GOOGLE_CLIENT_ID` is correct
- [ ] Check your `GOOGLE_CLIENT_SECRET` is correct
- [ ] Go back to Google Cloud Console
- [ ] Verify redirect URIs include:
  - [ ] `http://localhost:5000/oauth/google/callback`
  - [ ] `http://127.0.0.1:5000/oauth/google/callback`

### Issue: "ImportError: No module named 'authlib'"
**Solution:**
- [ ] Make sure venv is activated
- [ ] Run: `pip install Flask-Authlib python-dotenv`
- [ ] Check requirements.txt updated

### Issue: "Credentials not found"
**Solution:**
- [ ] Make sure .env file exists in project root
- [ ] Check variable names:
  - [ ] `GOOGLE_CLIENT_ID`
  - [ ] `GOOGLE_CLIENT_SECRET`
- [ ] Don't use quotes in .env file

### Issue: "No module named 'dotenv'"
**Solution:**
- [ ] Run: `pip install python-dotenv`
- [ ] Run: `pip freeze > requirements.txt`

### Issue: User can't see Google button
**Solution:**
- [ ] Check you updated login.html
- [ ] Refresh browser (hard refresh: Ctrl+F5)
- [ ] Check browser console for JavaScript errors

### Issue: "user_info is None"
**Solution:**
- [ ] Check scopes in Google Cloud Console include:
  - [ ] `openid`
  - [ ] `email`
  - [ ] `profile`
- [ ] In app.py, check OAuth config has correct scopes

---

## Step 6: Production Checklist (when deploying)

- [ ] Move .env values to environment variables
- [ ] Change redirect URI to your domain
- [ ] Update Google Cloud Console with production URL
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS only (Google requires it)
- [ ] Add error logging
- [ ] Test with real Google account

---

## What You've Accomplished! 🎉

✅ Created Google Cloud project
✅ Generated OAuth credentials
✅ Updated Flask app with OAuth support
✅ Updated templates with Google button
✅ Tested Google login and registration
✅ Users can now sign up/in with Google!

---

## Next Steps

### Option A: Add Microsoft OAuth (similar process)
- [ ] Create Azure app registration
- [ ] Get credentials
- [ ] Add Microsoft routes to app.py
- [ ] Update templates
- [ ] Test

### Option B: Add GitHub OAuth (similar process)
- [ ] Register OAuth app on GitHub
- [ ] Get credentials
- [ ] Add GitHub routes to app.py
- [ ] Update templates
- [ ] Test

### Option C: Add Account Linking
- [ ] Allow users to connect multiple providers
- [ ] Add "Connect Account" buttons on profile page
- [ ] Allow unlinking accounts
- [ ] Test switching between providers

---

## Helpful Resources

- Google OAuth Docs: https://developers.google.com/identity/protocols/oauth2
- Flask-Authlib Docs: https://docs.authlib.org/en/latest/
- Google Cloud Console: https://console.cloud.google.com/
- OAuth 2.0 Explained: https://oauth.net/2/

---

**Status: Ready to implement!** 🚀

When you've completed this checklist, you'll have working Google OAuth! Let me know if you get stuck on any step. 💪