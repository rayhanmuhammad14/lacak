from flask import Flask, request
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Ganti <username>, <password>, dan <cluster-url> sesuai dengan info MongoDB Atlas-mu
client = MongoClient("mongodb+srv://randomrayhansmd:T9Kx6MUE3iTIotiF@cluster0.rj7k62j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Pilih database dan collection
db = client["logtracker"]
log_collection = db["data"]

@app.route('/')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    t = datetime.datetime.now(datetime.timezone.utc)

    log_entry = {
        "timestamp": t,
        "ip": ip,
        "user_agent": ua
    }

    # Simpan ke MongoDB
    log_collection.insert_one(log_entry)

    return "Thanks!!"

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
