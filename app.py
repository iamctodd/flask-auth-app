from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import datetime
import os
import requests
import json
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
# Use PostgreSQL in production, SQLite in development
database_url = os.getenv('DATABASE_URL')
if not database_url:
    database_url = 'sqlite:///auth.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url

# Fix PostgreSQL URL format if needed
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Initialize database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model to store user information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # nullable for OAuth users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # OAuth fields
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    microsoft_id = db.Column(db.String(120), unique=True, nullable=True)
    github_id = db.Column(db.String(120), unique=True, nullable=True)
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return self.password_hash and check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


# ==================== AUTHENTICATION HELPERS ====================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_google_provider_cfg():
    """Get Google's OpenID configuration"""
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - protected route"""
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/oauth/google')
def oauth_google():
    """Redirect to Google OAuth consent page"""
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    redirect_uri = url_for("oauth_google_callback", _external=True, _scheme='https')
    
    request_uri = authorization_endpoint + "?" + urlencode({
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
    })
    return redirect(request_uri)

@app.route('/oauth/google/callback')
def oauth_google_callback():
    """Handle Google OAuth callback"""
    code = request.args.get("code")
    
    if not code:
        flash('Google authentication failed', 'danger')
        return redirect(url_for('login'))
    
    try:
        # Get token from Google
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        
        token_payload = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": url_for("oauth_google_callback", _external=True, _scheme='https'),
        }
        
        token_response = requests.post(token_endpoint, data=token_payload)
        tokens = token_response.json()
        
        if "error" in tokens:
            flash('Failed to get token from Google', 'danger')
            return redirect(url_for('login'))
        
        # Get user info
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {tokens['access_token']}"})
        
        user_info = userinfo_response.json()
        
        if not user_info.get('email'):
            flash('Failed to get user info from Google', 'danger')
            return redirect(url_for('login'))
        
        email = user_info.get('email')
        google_id = user_info.get('sub')
        username = email.split('@')[0]
        
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
            flash('This email is already registered. Please log in with your regular account first.', 'warning')
            return redirect(url_for('login'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            google_id=google_id
        )
        
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

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== APP INITIALIZATION ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)