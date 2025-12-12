# OAuth Implementation Guide

This guide covers adding Google, Microsoft, and GitHub OAuth to your Flask app step-by-step.

## Overview

We'll be using **Flask-Authlib** for OAuth, which handles:
- OAuth 2.0 authorization flow
- Token management
- User info retrieval
- Account linking

## Step 0: Install OAuth Dependencies

When ready, run:
```bash
pip install Flask-Authlib python-dotenv
```

Update `requirements.txt`:
```
Flask-Authlib==1.2.1
python-dotenv==1.0.0
```

## Architecture

Each OAuth provider will have:
1. **Setup**: Configure credentials in provider's console
2. **Config**: Add credentials to `.env` file
3. **Routes**: Login and callback routes
4. **User Linking**: Connect OAuth account to existing user or create new

## Step-by-Step Implementation Plan

### Step 1: Google OAuth
**Time: ~30-45 minutes**

1. Create Google Cloud project
2. Get OAuth 2.0 credentials
3. Add Google login button
4. Implement Google callback and user creation/linking
5. Test authentication flow

### Step 2: Microsoft OAuth
**Time: ~30-45 minutes**

1. Create Azure app registration
2. Get OAuth 2.0 credentials
3. Add Microsoft login button
4. Implement Microsoft callback and user creation/linking
5. Test authentication flow

### Step 3: GitHub OAuth
**Time: ~20-30 minutes**

1. Register OAuth App in GitHub
2. Get Client ID and Secret
3. Add GitHub login button
4. Implement GitHub callback and user creation/linking
5. Test authentication flow

### Step 4: Account Linking
**Time: ~45-60 minutes**

1. Add "Connect Account" feature on profile page
2. Allow users to link multiple OAuth providers
3. Add account unlinking
4. Display connected accounts on profile

## File Changes Preview

### New Files to Create
```
├── oauth_config.py         # OAuth provider configurations
├── .env                    # Store OAuth credentials (NOT in git)
├── .env.example            # Template for .env
└── templates/
    └── oauth_buttons.html  # Shared OAuth button component
```

### Files to Modify
```
├── app.py                  # Add OAuth routes
├── templates/
    ├── login.html          # Add OAuth buttons
    ├── register.html       # Add OAuth signup
    └── profile.html        # Add account linking
```

## Environment Variables Template

Create `.env` file:
```bash
# Flask Config
SECRET_KEY=your-secret-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

**Important**: Add `.env` to `.gitignore`

## OAuth Flow Diagram

```
User clicks "Login with Google"
    ↓
Redirect to Google OAuth consent page
    ↓
User approves permissions
    ↓
Google redirects to /oauth/google/callback with authorization code
    ↓
Exchange authorization code for access token
    ↓
Use access token to get user info (email, name, etc.)
    ↓
Check if user exists by Google ID
    ├─ Yes → Log user in
    └─ No → Create new user OR Link to existing user
    ↓
Redirect to dashboard
```

## Security Considerations

1. **HTTPS Only**: OAuth requires HTTPS in production
2. **State Parameter**: Prevent CSRF attacks (Authlib handles this)
3. **Scopes**: Request minimal scopes (email, profile only)
4. **Token Storage**: Don't store tokens in session (security risk)
5. **ID Verification**: Verify email before linking accounts

## Testing OAuth Locally

For local testing, you'll need:
1. Proper redirect URIs set in OAuth provider settings
2. Valid OAuth credentials
3. HTTPS tunnel (ngrok) for some providers that require HTTPS

Example ngrok setup:
```bash
ngrok http 5000
# Use ngrok URL for redirect URIs in provider settings
```

## Rollout Plan

**Week 1:**
- Setup Google OAuth
- Test Google login flow
- Update login/register pages

**Week 2:**
- Setup Microsoft OAuth
- Test Microsoft login flow
- Add multiple provider support

**Week 3:**
- Setup GitHub OAuth
- Test GitHub login flow
- Test all three together

**Week 4:**
- Implement account linking
- Add disconnect functionality
- Polish UI/UX

---

**Ready to start?** Let me know which provider you'd like to implement first! 🚀

I can provide:
1. Step-by-step Google OAuth setup
2. Complete code for OAuth callback handling
3. Updated templates with OAuth buttons
4. Account linking functionality
5. Testing checklist