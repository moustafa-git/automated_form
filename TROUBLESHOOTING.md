# Troubleshooting Vercel Deployment

## Current Error: FUNCTION_INVOCATION_FAILED

This guide will help you debug and fix the serverless function crash.

## Step 1: Check Vercel Logs

1. Go to your Vercel dashboard
2. Click on your project
3. Go to **"Functions"** tab
4. Click on the failed function
5. **Copy the full error message** - this will tell us exactly what's wrong

Common errors you might see:

### Error: "ModuleNotFoundError"
- **Cause:** Missing dependency in `requirements.txt`
- **Fix:** Add the missing package to `requirements.txt` and redeploy

### Error: "GOOGLE_CREDENTIALS_JSON not set"
- **Cause:** Environment variable not configured
- **Fix:** Add `GOOGLE_CREDENTIALS_JSON` in Vercel project settings → Environment Variables

### Error: "GOOGLE_SHEET_ID not set"
- **Cause:** Environment variable not configured
- **Fix:** Add `GOOGLE_SHEET_ID` in Vercel project settings → Environment Variables

### Error: Import errors
- **Cause:** Path issues or missing files
- **Fix:** Check that all files are in the repository

## Step 2: Verify Environment Variables

In Vercel dashboard → Your Project → Settings → Environment Variables, make sure you have:

1. **`GOOGLE_SHEET_ID`**
   - Value: Your Google Spreadsheet ID (from the URL)
   - Example: `1a2b3c4d5e6f7g8h9i0j`

2. **`GOOGLE_CREDENTIALS_JSON`**
   - Value: The complete JSON from your service account key file
   - Must be a single-line JSON string
   - Example: `{"type":"service_account","project_id":"...","private_key_id":"...",...}`

3. **`SHEET_NAME`** (optional)
   - Value: `SHOC` (or your sheet tab name)

## Step 3: Test with Simple Handler

If the Flask handler is causing issues, try this minimal test first:

Create `api/test.py`:
```python
def handler(req):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Hello from Vercel!'
    }
```

Update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/test.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/test.py"
    }
  ]
}
```

If this works, the issue is with the Flask integration.

## Step 4: Alternative - Use Serverless-Http

If Flask WSGI is causing issues, we can use `serverless-http`:

1. Add to `requirements.txt`:
   ```
   serverless-http
   ```

2. Update `api/index.py`:
   ```python
   import serverless_http
   from app import app
   
   handler = serverless_http(app)
   ```

## Step 5: Check File Structure

Make sure your repository has this structure:
```
.
├── api/
│   └── index.py
├── templates/
│   └── form.html
├── sheets_handler.py
├── requirements.txt
├── vercel.json
└── .gitignore
```

## Step 6: Common Fixes

### Fix 1: Missing Dependencies
```bash
# Check requirements.txt has:
flask
gspread
google-auth
```

### Fix 2: Path Issues
Make sure `sheets_handler.py` is in the root directory, not in `api/`

### Fix 3: Template Path
Verify `templates/form.html` exists and is in the `templates/` folder

### Fix 4: Environment Variables Format
- `GOOGLE_CREDENTIALS_JSON` must be the **entire JSON as a string**
- Use Vercel's JSON editor or paste as a single line
- No line breaks in the JSON string

## Step 7: Get Detailed Error

Add this to the top of `api/index.py` to see the actual error:

```python
import sys
import traceback

def handler(req):
    try:
        # ... your code ...
    except Exception as e:
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'traceback': traceback.format_exc(),
            'request_path': req.path if req else 'N/A',
            'request_method': req.method if req else 'N/A'
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(error_details, indent=2)
        }
```

## Still Not Working?

1. **Share the exact error from Vercel logs**
2. **Check that all files are committed to Git**
3. **Verify environment variables are set correctly**
4. **Try deploying a minimal Flask app first to test the setup**

## Quick Test Deployment

To test if Vercel Python works at all, create this minimal `api/index.py`:

```python
def handler(req):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '<h1>Vercel Python Works!</h1>'
    }
```

If this works, the issue is with Flask integration. If this fails, there's a Vercel configuration issue.

