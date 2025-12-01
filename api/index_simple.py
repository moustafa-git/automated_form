"""
Alternative handler using serverless-http for better Vercel compatibility
Use this if the main handler doesn't work
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import serverless_http
    from app import app
    
    # Wrap Flask app with serverless-http
    handler = serverless_http(app)
except ImportError:
    # Fallback if serverless-http not available
    def handler(req):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Error: serverless-http not installed. Add it to requirements.txt'
        }

