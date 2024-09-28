import re
from flask import Flask, request, abort, jsonify
from flask_limiter import Limiter
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
limiter = Limiter(
    key_func=lambda: request.remote_addr,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

def detect_sql_injection(query_string):
    sql_patterns = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",  
        r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))", 
        r"\bSELECT\b.*\bFROM\b.*\bWHERE\b",
        r"\b(UNION|JOIN|INSERT|UPDATE|DELETE)\b",  
        r"(\%2B|\+|=)\s*(\%27|')\s*(OR|AND)", 
        r"(\bWAITFOR\b\s+\bDELAY\b\s*\()|(\bSLEEP\b\s*\()",  
    ]
    for pattern in sql_patterns:
        if re.search(pattern, query_string, re.IGNORECASE):
            return True
    return False

def detect_xss(payload):
    xss_patterns = [
        r"<script\b[^>]*>(.*?)</script>", 
        r"(\%3Cscript\%3E)", 
        r"(<img.*?onerror\s*=\s*['\"](.*?)['\"])",  
        r"(<svg.*?onload\s*=\s*['\"](.*?)['\"])", 
        r"javascript:",  
        r"data:text/html,", 
    ]
    for pattern in xss_patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            return True
    return False

def detect_bad_user_agent(user_agent):
    print(user_agent)
    bad_agents = [
        'sqlmap', 
        'nmap', 
        'nikto', 
        'Burp Suite',  
        'fuzz',        
        'ZAP',         
        'dirbuster',   
    ]
    for agent in bad_agents:
        if agent.lower() in user_agent.lower():
            return True
    return False

@app.before_request
@limiter.limit("5 per minute")  # Membatasi 5 permintaan per menit
def security_checks():
    user_agent = request.headers.get('User-Agent', '')
    query_string = request.query_string.decode('utf-8')

    if detect_bad_user_agent(user_agent):
        abort(403, description="Forbidden: Bad User-Agent Detected")

    if detect_sql_injection(query_string):
        abort(403, description="Forbidden: SQL Injection Attempt Detected")

    for key, value in request.values.items():
        if detect_xss(value):
            abort(403, description="Forbidden: XSS Attempt Detected")

    if any(not value.strip() for value in request.values.values()):
        abort(400, description="Bad Request: Empty Input Detected")

@app.route('/')
def home():
    return "Welcome to the secured site!"

if __name__ == '__main__':
    app.run(debug=True)
