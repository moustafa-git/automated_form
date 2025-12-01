# Deploy to Vercel - Step by Step Guide

Vercel is **100% free** for personal projects and provides:
- ✅ Free HTTPS
- ✅ Global CDN
- ✅ Automatic deployments from GitHub
- ✅ No credit card required

## Important: Excel File Limitation

**Vercel's serverless environment is read-only** - you cannot write to local files. 

**Solution:** We'll use **Google Sheets** instead of Excel (free, works the same way).

---

## Step 1: Set Up Google Sheets API (Free)

### 1.1 Create a Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create a new project (or use existing)
3. Enable **Google Sheets API** and **Google Drive API**:
   - Go to "APIs & Services" → "Library"
   - Search "Google Sheets API" → Enable
   - Search "Google Drive API" → Enable

### 1.2 Create Service Account (for automated access)

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name it (e.g., "vercel-sheets") → Create
4. Click on the service account → "Keys" tab
5. Click "Add Key" → "Create new key" → **JSON**
6. **Download the JSON file** - you'll need this!

### 1.3 Create Google Sheet

1. Go to https://sheets.google.com
2. Create a new spreadsheet
3. Name it (e.g., "SHOC Tracker")
4. **Copy the Spreadsheet ID** from the URL:
   - URL looks like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit`
   - Copy the part between `/d/` and `/edit`

### 1.4 Share Sheet with Service Account

1. Open your Google Sheet
2. Click "Share" button
3. **Paste the service account email** (from the JSON file, field: `client_email`)
4. Give it **Editor** permission
5. Click "Send"

### 1.5 Prepare Your Sheet Structure

Make sure your Google Sheet has this structure:
- **Row 1:** Title (e.g., "SHOC Register/Action Tracker")
- **Row 2:** Blank
- **Row 3:** Headers: `S/N`, `Date`, `Observer`, `Company`, `Trade/Position`, `Observation Group`, `Location/Area`, `Observation Type`, `Observation`, `Action`, `Action Taken`, `Corrective Action / Preventive Action`, `Priority`, `Risk Rating`, `Custodian`, `Due Date`, `Status`, `Comment`
- **Row 4+:** Data rows (will be auto-filled)

---

## Step 2: Prepare Your Code for Vercel

Your code is already set up! The files are:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `sheets_handler.py` - Google Sheets integration
- ✅ `requirements.txt` - Updated with Google Sheets libraries

---

## Step 3: Deploy to Vercel

### 3.1 Push Code to GitHub

```bash
cd "D:\automated form"
git init
git add .
git commit -m "Ready for Vercel deployment"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 3.2 Deploy on Vercel

1. Go to https://vercel.com
2. Sign up/login (free, no card needed)
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Vercel will auto-detect Python settings
6. **Before deploying, add environment variables:**

### 3.3 Set Environment Variables in Vercel

In Vercel project settings → "Environment Variables", add:

1. **`GOOGLE_SHEET_ID`**
   - Value: Your spreadsheet ID (from Step 1.3)

2. **`GOOGLE_CREDENTIALS_JSON`**
   - Value: The **entire contents** of the JSON file you downloaded (Step 1.2)
   - **Important:** Paste the whole JSON as a single-line string, or use Vercel's JSON editor

3. **`SHEET_NAME`** (optional)
   - Value: `SHOC` (or your sheet tab name)

### 3.4 Deploy

1. Click "Deploy"
2. Wait 1-2 minutes
3. **Your app is live!** URL: `https://your-project.vercel.app`

---

## Step 4: Test Your Deployment

1. Visit your Vercel URL
2. Fill out the form
3. Submit
4. Check your Google Sheet - you should see a new row!

---

## Troubleshooting

### Error: "GOOGLE_CREDENTIALS_JSON not set"
- Make sure you added the environment variable in Vercel
- The JSON must be the complete file contents

### Error: "Sheet not found"
- Check that `SHEET_NAME` matches your Google Sheet tab name exactly
- Default is "SHOC"

### Error: "Permission denied"
- Make sure you shared the Google Sheet with the service account email
- Service account needs "Editor" permission

### Form submits but no data appears
- Check Vercel function logs (in Vercel dashboard → Functions tab)
- Verify the Google Sheet ID is correct

---

## Local Testing (Optional)

To test Google Sheets integration locally:

1. Create a `.env` file:
   ```
   GOOGLE_SHEET_ID=your_spreadsheet_id
   GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
   SHEET_NAME=SHOC
   ```

2. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

3. Update `app.py` to load `.env`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

## Benefits of Google Sheets vs Excel

- ✅ **Free forever**
- ✅ **Real-time collaboration**
- ✅ **Accessible from anywhere**
- ✅ **No file uploads needed**
- ✅ **Automatic backups**
- ✅ **Can export to Excel anytime**

---

## Need Help?

If you get stuck, check:
- Vercel function logs in dashboard
- Google Cloud Console for API errors
- Make sure all environment variables are set correctly

