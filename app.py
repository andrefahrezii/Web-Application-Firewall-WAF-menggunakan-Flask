from flask import Flask, request, render_template
from waf.detector import analyze_request

app = Flask(__name__)

@app.before_request
def waf_middleware():
    detection_result = analyze_request(request)
    if detection_result:
        return f"Request Blocked: {detection_result}", 403

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
