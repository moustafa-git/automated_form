# Deployment Guide - SHOC Observation Form

This guide explains how to make your Flask app accessible online.

## Option 1: Quick Testing with ngrok (5 minutes)

**Best for:** Immediate testing, sharing with team temporarily

### Steps:
1. **Install ngrok:**
   - Download from https://ngrok.com/download
   - Extract and add to PATH, or run from extracted folder

2. **Start your Flask app:**
   ```bash
   python app.py
   ```

3. **In a new terminal, start ngrok:**
   ```bash
   ngrok http 5000
   ```

4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`) and share it!

**Note:** Free ngrok URLs change each time you restart. For permanent URLs, use Option 2 or 3.

---

## Option 2: Deploy to Render (Free Tier Available)

**Best for:** Permanent free hosting, easy setup

### Steps:

1. **Create a GitHub repository:**
   - Go to https://github.com
   - Create a new repo
   - Push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin YOUR_REPO_URL
     git push -u origin main
     ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/login (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name:** shoc-form (or any name)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free
   - Click "Create Web Service"

3. **Upload Excel file:**
   - After deployment, go to your service dashboard
   - Use Render's shell or file upload feature to add `simple.xlsx`
   - Or use environment variables to point to a cloud storage (S3, etc.)

4. **Your app is live!** Render gives you a URL like `https://shoc-form.onrender.com`

---

## Option 3: Deploy to Railway (Free Tier Available)

**Best for:** Simple deployment, good free tier

### Steps:

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Upload Excel file:**
   - Use Railway's file system or connect to cloud storage

5. **Get your URL** from Railway dashboard

---

## Option 4: Deploy to PythonAnywhere (Free Tier Available)

**Best for:** Python-focused hosting, simple file upload

### Steps:

1. **Sign up at https://www.pythonanywhere.com** (free account)

2. **Upload your files:**
   - Go to Files tab
   - Upload `app.py`, `requirements.txt`, `simple.xlsx`, and `templates/form.html`

3. **Open Bash console** and install dependencies:
   ```bash
   pip3.10 install --user flask openpyxl gunicorn
   ```

4. **Create a Web App:**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose Flask, Python 3.10
   - Set source code to `/home/YOUR_USERNAME/mysite/app.py`

5. **Configure WSGI file:**
   - Edit the WSGI file to point to your app
   - Reload the web app

6. **Your app is live!** URL: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Important Notes for All Deployments:

### Excel File Location:
- **Local development:** Uses `D:\automated form\simple.xlsx`
- **Cloud deployment:** The Excel file must be uploaded to the server
- **Better solution:** Use cloud storage (AWS S3, Google Drive API, etc.) for production

### Environment Variables (Optional):
You can set these in your hosting platform:
- `EXCEL_PATH` - Path to Excel file (defaults to `simple.xlsx` in app directory)
- `SHEET_NAME` - Sheet name (defaults to `SHOC`)
- `PORT` - Server port (defaults to 5000)
- `FLASK_DEBUG` - Set to `true` for debug mode (defaults to `False`)

### Security:
- Remove `debug=True` in production
- Consider adding authentication if the form is public
- Use HTTPS (most platforms provide this automatically)

---

## Recommended: Render (Easiest Free Option)

For a quick permanent deployment, I recommend **Render**:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy GitHub integration
- ✅ Simple file upload via dashboard
- ✅ Auto-deploys on git push

Follow **Option 2** above for step-by-step instructions.

