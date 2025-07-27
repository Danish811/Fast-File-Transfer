import os
import socket
import qrcode
import webbrowser
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory, jsonify

# --- Firebase Server Setup ---
# This uses the service account key file for server-side operations.
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Successfully connected to Firestore with admin credentials.")
except Exception as e:
    print(f"!!! FIREBASE ADMIN SETUP ERROR !!!")
    print(f"Could not initialize Firebase Admin: {e}")
    print("Please ensure 'serviceAccountKey.json' is in the correct folder.")
    db = None

# --- Firebase Client Config ---
# IMPORTANT: PASTE YOUR FIREBASE CLIENT CONFIG VALUES HERE
# Find these in your Firebase Project Settings -> General tab -> Your Web App -> Config
FIREBASE_CONFIG_CLIENT = {
    "apiKey": "AIzaSyCQQREb9BS7egQmnxnn4J_GVwixsvIVHvw",
    "authDomain": "mobile-pc-clipboard.firebaseapp.com",
    "projectId": "mobile-pc-clipboard",
    "storageBucket": "mobile-pc-clipboard.appspot.com",
    "messagingSenderId": "801454272408",
    "appId": "1:801454272408:web:e1e1a09c59be85378905ed",
    "measurementId": "G-SN0HL7C4XX"
}


# --- App Folder Configuration ---
APP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pc_mobile_transfer')
UPLOAD_FOLDER = os.path.join(APP_FOLDER, 'SHARING')
DOWNLOAD_FOLDER = os.path.join(APP_FOLDER, 'SHARING')

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = 'a_very_secret_key'

# --- Helper Function ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# --- Main Routes ---
@app.route('/')
def home():
    """Renders the main landing page which links to other tools."""
    return render_template('index.html')

@app.route('/files')
def files_page():
    """Renders the file transfer page."""
    try:
        files = sorted(os.listdir(DOWNLOAD_FOLDER), key=lambda f: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, f)), reverse=True)
    except FileNotFoundError:
        files = []
    return render_template('file_transfer.html', downloadable_files=files)

# --- File Transfer Logic ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file selected!', 'error')
    else:
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash(f'Successfully uploaded: {file.filename}', 'success')
    return redirect(url_for('files_page'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# --- Live Clipboard Logic ---
@app.route('/clipboard')
def clipboard_page():
    """Renders the live clipboard page."""
    if not db:
        flash("Firestore Admin SDK is not connected. Clipboard will not work.", "error")
        return redirect(url_for('home'))
        
    # Pass the user-configured Firebase config to the template
    return render_template('clipboard.html', firebase_config=FIREBASE_CONFIG_CLIENT)

# This endpoint is no longer needed as the client writes directly to Firestore
# @app.route('/update_clipboard', methods=['POST']) ...

# --- Main Execution ---
if __name__ == '__main__':
    for folder in [APP_FOLDER, UPLOAD_FOLDER, DOWNLOAD_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")

    host_ip = get_local_ip()
    port = 5000
    url = f"http://{host_ip}:{port}"

    # Generate QR code only if not in debug mode to avoid re-running on save
    if not app.debug:
        qr_img_path = os.path.join(APP_FOLDER, "qr_code.png")
        qrcode.make(url).save(qr_img_path)
        print("--- PC-Mobile Two-Way Transfer Server ---")
        print(f"\n[SERVER RUNNING ON] -> {url}")
        print(f"Scan the QR code image that opened to access the app on your phone.")
        print("Press CTRL+C in this terminal to stop the server.")
        print("-" * 40)
        webbrowser.open(qr_img_path)
    
    app.run(host='0.0.0.0', port=port, debug=True)
