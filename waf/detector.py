from .rules import detect_sql_injection, detect_xss, detect_bad_user_agent

def analyze_request(request):
    query_string = request.query_string.decode()
    payload = request.get_data(as_text=True)
    user_agent = request.headers.get('User-Agent', '')

    if detect_sql_injection(query_string):
        return "SQL Injection detected"

    if detect_xss(payload):
        return "XSS detected"

    if detect_bad_user_agent(user_agent):
        return f"Blocked User-Agent: {user_agent}"

    return None
