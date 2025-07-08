from flask import Flask, request, render_template_string
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://randomrayhansmd:T9Kx6MUE3iTIotiF@cluster0.rj7k62j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["logtracker"]
log_collection = db["data"]

# Halaman utama: tombol untuk ambil lokasi
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tracking Lokasi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body>
        <h3>Tekan tombol di bawah untuk mengirim lokasi 📍</h3>
        <button onclick="getLocation()">Izinkan dan Kirim Lokasi</button>
        <p id="status"></p>

        <script>
        function getLocation() {
            document.getElementById('status').innerText = "Meminta izin lokasi...";
            navigator.geolocation.getCurrentPosition(pos => {
                fetch("/log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        latitude: pos.coords.latitude,
                        longitude: pos.coords.longitude,
                        accuracy: pos.coords.accuracy
                    })
                }).then(res => res.text()).then(msg => {
                    document.getElementById('status').innerText = msg;
                });
            }, err => {
                document.getElementById('status').innerText = "❌ Izin lokasi ditolak.";
            });
        }
        </script>
    </body>
    </html>
    ''')

# Endpoint untuk menyimpan lokasi ke MongoDB
@app.route('/log', methods=['POST'])
def log_location():
    data = request.get_json()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    t = datetime.datetime.now(datetime.timezone.utc)

    log_entry = {
        "timestamp": t,
        "ip": ip,
        "user_agent": ua,
        "location": {
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
            "accuracy": data.get("accuracy")
        }
    }

    log_collection.insert_one(log_entry)
    return "✅ Lokasi berhasil disimpan!"

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
