import sys
import os
from pathlib import Path
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, redirect, url_for
from sheets_handler import append_to_sheets

# Initialize Flask app
app = Flask(__name__, 
            template_folder=str(Path(__file__).parent.parent / 'templates'),
            static_folder=str(Path(__file__).parent.parent / 'static'))

@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    form_data = {
        "title": request.form.get("title") or "",
        "safe_act": request.form.get("safe_act") or "",
        "positive_action": request.form.get("positive_action") or "",
        "unsafe_act": request.form.get("unsafe_act") or "",
        "immediate_corrective": request.form.get("immediate_corrective") or "",
        "preventive_action": request.form.get("preventive_action") or "",
        "observer": request.form.get("observer") or "",
        "company": request.form.get("company") or "",
        "date_occurred": request.form.get("date_occurred") or "",
        "location_area": request.form.get("location_area") or "",
        "trade_position": request.form.get("trade_position") or "",
        "observation_group": request.form.get("observation_group") or "",
        "observation_type": request.form.get("observation_type") or "",
        "observation": request.form.get("observation") or "",
        "action": request.form.get("action") or "",
        "action_taken": request.form.get("action_taken") or "",
        "corrective_preventive_action": request.form.get("corrective_preventive_action") or "",
        "priority": request.form.get("priority") or "",
        "risk_rating": request.form.get("risk_rating") or "",
        "custodian": request.form.get("custodian") or "",
        "due_date": request.form.get("due_date") or "",
        "status": request.form.get("status") or "",
        "comment": request.form.get("comment") or "",
    }

    try:
        append_to_sheets(form_data)
        return redirect(url_for("index"))
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return error_msg, 500

# Vercel serverless function handler
def handler(req):
    """Handle Vercel serverless function requests"""
    try:
        # Get request details
        method = req.method or 'GET'
        path = req.path or '/'
        headers = req.headers or {}
        body = req.body or b''
        
        # Parse query string
        query_string = ''
        if '?' in path:
            path, query_string = path.split('?', 1)
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body if isinstance(body, bytes) else body.encode()),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers to environ
        for key, value in headers.items():
            key_upper = key.upper().replace('-', '_')
            if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                environ[f'HTTP_{key_upper}'] = value
        
        # Create request context and dispatch
        with app.request_context(environ):
            response = app.full_dispatch_request()
            
            # Convert Flask response to Vercel format
            response_headers = dict(response.headers)
            response_body = response.get_data(as_text=True)
            
            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body
            }
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f"Internal Server Error\n\nError: {str(e)}\n\n{error_trace}"
        }
