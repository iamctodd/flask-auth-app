# Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FLASK AUTH APP                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Flask Application (app.py)                │   │
│  │  ┌──────────────┐      ┌──────────────┐            │   │
│  │  │   Routes     │      │  Decorators  │            │   │
│  │  │ - /register  │      │ - @app.route │            │   │
│  │  │ - /login     │      │ - @login_req │            │   │
│  │  │ - /dashboard │      │              │            │   │
│  │  │ - /profile   │      │              │            │   │
│  │  │ - /logout    │      │              │            │   │
│  │  └──────────────┘      └──────────────┘            │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │         User Model (SQLAlchemy ORM)          │  │   │
│  │  │  - id, username, email                       │  │   │
│  │  │  - password_hash                             │  │   │
│  │  │  - google_id, microsoft_id, github_id        │  │   │
│  │  │  Methods: set_password(), check_password()   │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↓                                 │
│                 ┌──────────────────────┐                    │
│                 │  SQLite Database     │                    │
│                 │  (auth.db)           │                    │
│                 │  - users table       │                    │
│                 └──────────────────────┘                    │
│                           ↓                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      Templates (HTML + Bootstrap 5)                │   │
│  │  ┌──────────────┐  ┌──────────────┐               │   │
│  │  │ Auth Pages   │  │ User Pages   │               │   │
│  │  │ - login      │  │ - dashboard  │               │   │
│  │  │ - register   │  │ - profile    │               │   │
│  │  │ - base       │  │              │               │   │
│  │  └──────────────┘  └──────────────┘               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Session Management                        │   │
│  │  - user_id stored in session                       │   │
│  │  - username stored in session                      │   │
│  │  - email stored in session                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Registration Flow

```
┌─────────────────────────────────────────────────────────────┐
│  User visits /register                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Displays registration form (register.html)                │
│  - Username field                                           │
│  - Email field                                              │
│  - Password field                                           │
│  - Confirm password field                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  User submits form (POST /register)                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Server-side Validation                                     │
│  ✓ All fields required?                                    │
│  ✓ Passwords match?                                        │
│  ✓ Password >= 6 chars?                                    │
│  ✓ Username unique?                                        │
│  ✓ Email unique?                                           │
└─────────────────────────────────────────────────────────────┘
                    ↙           ↘
              VALID              INVALID
                ↓                  ↓
        ┌──────────────┐  ┌──────────────────┐
        │ Hash password│  │ Show error msg   │
        │ Save to DB   │  │ Redirect to form │
        │ Commit       │  └──────────────────┘
        └──────────────┘
                ↓
        ┌──────────────┐
        │ Flash: Success
        │ Redirect to  │
        │ /login       │
        └──────────────┘
                ↓
        Account Created! ✅
```

---

## Login Flow

```
┌─────────────────────────────────────────────────────────────┐
│  User visits /login                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Displays login form (login.html)                          │
│  - Username field                                           │
│  - Password field                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  User submits form (POST /login)                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Lookup user by username in database                       │
└─────────────────────────────────────────────────────────────┘
                    ↙           ↘
              FOUND              NOT FOUND
                ↓                  ↓
        ┌──────────────┐  ┌──────────────────┐
        │ Check password  │  │ Flash: Invalid   │
        │ hash matches?   │  │ credentials      │
        └──────────────┘  │ Redirect to login│
                ↓          └──────────────────┘
            ↙   ↘
        MATCH   MISMATCH
          ↓       ↓
      CREATE   FLASH:
      SESSION  ERROR
          ↓
    Set user_id
    Set username
    Set email
        ↓
    REDIRECT to
    /dashboard
        ↓
    User Logged In! ✅
```

---

## Protected Route Flow

```
┌─────────────────────────────────────────────────────────────┐
│  User requests protected route (e.g., /dashboard)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  @login_required decorator intercepts                      │
│  Checks: Is user_id in session?                           │
└─────────────────────────────────────────────────────────────┘
                    ↙           ↘
            HAS user_id          NO user_id
                ↓                  ↓
        ┌──────────────┐  ┌──────────────────┐
        │ Load user    │  │ Flash: "Please   │
        │ from DB      │  │ log in first"    │
        │ Render page  │  │ Redirect to /lgn │
        │ User sees    │  └──────────────────┘
        │ dashboard    │
        └──────────────┘
                ↓
    Protected page displayed! ✅
```

---

## Authentication State Machine

```
                    ┌──────────────┐
                    │  NOT LOGGED  │
                    │     IN       │
                    └──────────────┘
                         ↑    ↓
                 Logout  │    │ Login
                         │    │ Success
                         │    ↓
                    ┌──────────────┐
                    │  LOGGED IN   │
                    │   (Session   │
                    │   Active)    │
                    └──────────────┘
                         ↑    ↓
                Session │    │ Session
                Expires │    │ Invalid
                         │    ↓
                    ┌──────────────┐
                    │ SESSION ENDED│
                    └──────────────┘
                         ↓
                  Redirect to Home
```

---

## Database Schema

```
┌─────────────────────────────────────┐
│            users Table              │
├─────────────────────────────────────┤
│ id (PK)             INTEGER         │
├─────────────────────────────────────┤
│ username (UNIQUE)   VARCHAR(80)     │
├─────────────────────────────────────┤
│ email (UNIQUE)      VARCHAR(120)    │
├─────────────────────────────────────┤
│ password_hash       VARCHAR(255)    │
├─────────────────────────────────────┤
│ created_at          DATETIME        │
├─────────────────────────────────────┤
│ google_id (UNIQUE)  VARCHAR(120)    │ ← For OAuth
├─────────────────────────────────────┤
│ microsoft_id (UQ)   VARCHAR(120)    │ ← For OAuth
├─────────────────────────────────────┤
│ github_id (UNIQUE)  VARCHAR(120)    │ ← For OAuth
└─────────────────────────────────────┘

Legend:
PK = Primary Key
UQ = Unique
→ = Will be used in Phase 2
```

---

## Request/Response Cycle

```
CLIENT (Browser)          SERVER (Flask)           DATABASE
    │                          │                        │
    │  GET /register           │                        │
    │─────────────────────────→│                        │
    │                          │                        │
    │                    Render register.html           │
    │←─────────────────────────│                        │
    │ (HTML form)              │                        │
    │                          │                        │
    │  POST /register          │                        │
    │  (form data)             │                        │
    │─────────────────────────→│                        │
    │                          │ Validate data         │
    │                          │ Hash password         │
    │                          │ CREATE User           │
    │                          │───────────────────────→│
    │                          │                   INSERT
    │                          │←───────────────────────│
    │                          │ COMMIT                 │
    │                    Redirect to /login             │
    │←─────────────────────────│                        │
    │ (302 Found)              │                        │
    │                          │                        │
    │  GET /login              │                        │
    │─────────────────────────→│                        │
    │                    Render login.html              │
    │←─────────────────────────│                        │
    │ (HTML form)              │                        │
    │                          │                        │
    │  POST /login             │                        │
    │  (username, pwd)         │                        │
    │─────────────────────────→│                        │
    │                          │ Query user             │
    │                          │───────────────────────→│
    │                          │               SELECT *
    │                          │←───────────────────────│
    │                          │ Check password hash    │
    │                          │ Create session         │
    │                    Redirect to /dashboard         │
    │←─────────────────────────│                        │
    │ (302 Found)              │                        │
    │ Set-Cookie: session      │                        │
    │                          │                        │
    │  GET /dashboard          │                        │
    │  (Cookie: session)       │                        │
    │─────────────────────────→│                        │
    │                          │ Verify session         │
    │                          │ Query user             │
    │                          │───────────────────────→│
    │                          │               SELECT *
    │                          │←───────────────────────│
    │                    Render dashboard.html          │
    │←─────────────────────────│                        │
    │ (with user info)         │                        │
```

---

## OAuth Flow Preview (Phase 2)

```
When we add OAuth, the flow will be:

CLIENT          FLASK APP        OAUTH PROVIDER      DATABASE
   │                │                   │                │
   │ Click Google   │                   │                │
   │ Login Button   │                   │                │
   │────────────────→                   │                │
   │                │                   │                │
   │           Redirect to Google consent page            │
   │←────────────────────────────────────────────       │
   │                │                   │                │
   │             (User approves)        │                │
   │                ←───────────────────│                │
   │             Code + State           │                │
   │                │                   │                │
   │                │ Exchange code     │                │
   │                │ for token         │                │
   │                │──────────────────→│                │
   │                │                   │                │
   │                │         Access token               │
   │                │←──────────────────│                │
   │                │                   │                │
   │                │ Get user info     │                │
   │                │──────────────────→│                │
   │                │                   │                │
   │                │      User data    │                │
   │                │←──────────────────│                │
   │                │                   │                │
   │                │ Query by google_id                 │
   │                │───────────────────────────────────→│
   │                │                            SELECT *│
   │                │←───────────────────────────────────│
   │                │  (User found or create new)        │
   │                │ Create session                      │
   │                │                                     │
   │        Redirect to /dashboard (302)                 │
   │←────────────────────────────────────────────────   │
   │                                                      │
   │    GET /dashboard (with session cookie)              │
   │────────────────→                                    │
   │                  Dashboard rendered                 │
   │←────────────────────────────────────────────────   │
```

---

## File Dependency Graph

```
app.py
├── imports: Flask, SQLAlchemy, werkzeug.security
├── defines: User model
├── defines: login_required decorator
├── defines: all routes
│   ├── uses: templates/base.html
│   ├── uses: templates/index.html
│   ├── uses: templates/login.html
│   ├── uses: templates/register.html
│   ├── uses: templates/dashboard.html
│   ├── uses: templates/profile.html
│   ├── uses: templates/404.html
│   └── uses: templates/500.html
└── uses: SQLite (auth.db)

templates/base.html
├── extends: (base template)
├── includes: Bootstrap 5 CSS
├── includes: Bootstrap 5 JS
└── blocks: content (extended by child templates)

templates/login.html
├── extends: base.html
├── shows: login form (POST /login)
└── shows: OAuth provider buttons (placeholder)

templates/register.html
├── extends: base.html
└── shows: registration form (POST /register)

templates/dashboard.html
├── extends: base.html
├── requires: user_id in session
└── shows: user greeting & status

templates/profile.html
├── extends: base.html
├── requires: user_id in session
├── shows: user account info
└── shows: connected accounts (placeholder)

requirements.txt
├── Flask==3.0.0
├── Flask-SQLAlchemy==3.1.1
└── Werkzeug==3.0.1
```

---

## State Diagram for User Object

```
           ┌──────────────────────┐
           │   User Created       │
           │ (Not in DB yet)      │
           └──────────────────────┘
                      ↓
           ┌──────────────────────┐
           │ Properties Set:      │
           │ - username           │
           │ - email              │
           │ - password_hash      │
           └──────────────────────┘
                      ↓
           ┌──────────────────────┐
           │ Added to Session     │
           │ db.session.add()     │
           └──────────────────────┘
                      ↓
           ┌──────────────────────┐
           │ Committed to DB      │
           │ db.session.commit()  │
           │ Gets ID from DB      │
           └──────────────────────┘
                      ↓
           ┌──────────────────────┐
           │ Retrievable from DB  │
           │ User.query.get(id)   │
           └──────────────────────┘
                      ↓
           ┌──────────────────────┐
           │ Can Login            │
           │ Can Access Protected │
           │ Routes               │
           └──────────────────────┘
```

---

## Session Lifecycle

```
USER ACTION               SESSION STATE
┌─────────────────────────────────────────────────┐
│ Not logged in           │ user_id: empty         │
├─────────────────────────────────────────────────┤
│ Submits login form      │ Validating...          │
├─────────────────────────────────────────────────┤
│ Login successful        │ user_id: 1             │
│                         │ username: john         │
│                         │ email: john@ex.com     │
├─────────────────────────────────────────────────┤
│ Visiting /dashboard     │ Session verified ✓     │
│ (passes cookie)         │ User loaded from DB    │
├─────────────────────────────────────────────────┤
│ Browser closed          │ Session persists       │
│                         │ (until timeout/logout) │
├─────────────────────────────────────────────────┤
│ Revisit site            │ Session still valid    │
│ (cookie sent again)     │ User auto-logged in    │
├─────────────────────────────────────────────────┤
│ Clicks logout           │ session.clear()        │
│                         │ All data cleared       │
├─────────────────────────────────────────────────┤
│ After logout            │ user_id: empty         │
│                         │ Must log in again      │
└─────────────────────────────────────────────────┘
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│  SECURITY LAYERS (in order of defense)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: INPUT VALIDATION                                 │
│  ├─ All fields required?                                   │
│  ├─ Email format valid?                                    │
│  ├─ Password >= 6 chars?                                   │
│  └─ Username/email not already registered?                 │
│                                                              │
│  Layer 2: PASSWORD HASHING                                 │
│  ├─ Never store plain text passwords                       │
│  ├─ Use Werkzeug's generate_password_hash()                │
│  ├─ Automatic salting per user                             │
│  └─ Check with check_password_hash()                       │
│                                                              │
│  Layer 3: SESSION MANAGEMENT                               │
│  ├─ Server-side sessions (not client storage)              │
│  ├─ Secure session cookies                                 │
│  ├─ Check user_id in session on protected routes           │
│  └─ Clear session on logout                                │
│                                                              │
│  Layer 4: PROTECTED ROUTES                                 │
│  ├─ @login_required decorator                              │
│  ├─ Redirect non-authenticated users                       │
│  └─ Database query verification                            │
│                                                              │
│  Layer 5: READY FOR FUTURE                                 │
│  ├─ CSRF protection (Flask-WTF)                            │
│  ├─ Rate limiting                                          │
│  ├─ Email verification                                     │
│  └─ 2FA/MFA                                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

This visual documentation helps understand:
- ✅ How the app is structured
- ✅ How data flows through routes
- ✅ How authentication works
- ✅ Security layers in place
- ✅ What happens during OAuth (future)

Use these diagrams when explaining to others or when planning OAuth additions!