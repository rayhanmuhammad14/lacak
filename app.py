from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    t = datetime.datetime.now(datetime.timezone.utc)
    with open('log.txt', 'a') as f:
        f.write(f"[{t.isoformat()}] IP :{ip}, UA: {ua}\n")
    return "Thanks!!"

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)