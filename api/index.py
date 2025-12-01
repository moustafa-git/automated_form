import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, redirect, url_for
from sheets_handler import append_to_sheets

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
        return f"Error: {str(e)}", 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda status, headers: None)
