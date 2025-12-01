"""
Minimal test handler to verify Vercel Python runtime works
"""
def handler(req):
    """Simple test handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '''
        <html>
        <head><title>Vercel Test</title></head>
        <body>
            <h1>✅ Vercel Python Runtime Works!</h1>
            <p>If you see this, Vercel is working correctly.</p>
            <p>Request path: {}</p>
            <p>Request method: {}</p>
        </body>
        </html>
        '''.format(req.path if req else 'N/A', req.method if req else 'N/A')
    }

