# PC-Mobile Two-Way Transfer & Live Clipboard

A simple, self-hosted web application to seamlessly transfer files, text, and links between your PC and mobile phone over your local network.

## Features

* **Shared File Transfer Folder:**
    * A single `sharing` folder for two-way transfers.
    * Upload files from your phone, and they appear in the `sharing` folder on your PC.
    * Place files in the `sharing` folder on your PC, and they become instantly available for download on your phone.
* **Live Shared Clipboard:**
    * A real-time, shared text area powered by Firebase.
    * Type or paste on your PC, and it instantly appears on your phone (and vice-versa). Perfect for sharing links, notes, and snippets.
* **QR Code Connection:**
    * Run the server, and it automatically generates and displays a QR code.
    * Simply scan the code with your phone to connect instantly—no typing IP addresses.
* **Zero Mobile Data Usage:**
    * All file transfers happen directly over your local Wi-Fi network (including your phone's hotspot). **No mobile data is used for file transfers.**
* **Secure & Private:**
    * Your files and data never leave your local network. The clipboard functionality uses your own private Firebase project.

## How It Works

This project runs a lightweight web server on your PC using **Flask**.

1.  **Local Server:** When you run the Python script, it starts a server that listens for connections on your local network.
2.  **Local Connection:** By scanning the QR code, your phone's browser connects directly to your PC's local IP address (e.g., `192.168.x.x`).
3.  **File Transfer:** When you upload or download a file, the data travels directly between the browser on your phone and the server on your PC over the local Wi-Fi signal.
4.  **Live Clipboard:** The clipboard page uses a free **Firebase Realtime Database** as a middleman. Both your PC and phone browsers connect to this database. When one device writes text to the database, the other device is instantly notified and updates its display.

## Folder Structure

For the application to work correctly, your files must be organized as follows:

```
your-project-folder/
|
|-- transfer_server.py        # The main Python script
|-- serviceAccountKey.json    # Your private Firebase key
|
|-- templates/
|   |-- index.html            # The main landing page
|   |-- file_transfer.html    # The file transfer UI
|   |-- clipboard.html        # The shared clipboard UI
|
|-- pc_mobile_transfer/
    |-- qr_code.png           # Auto-generated QR code
    |
    |-- sharing/              # All shared files (to/from PC and mobile) appear here.
```

## Setup and Installation

Follow these steps to get the project running.

### 1. Prerequisites

* **Python 3:** Make sure you have Python installed on your PC. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Install Dependencies

1.  Open a terminal or command prompt in your main project folder.
2.  Install the required Python libraries:
    ```bash
    pip install Flask qrcode firebase-admin
    ```

### 3. Firebase Setup (for Live Clipboard)

This is a one-time setup that takes about 5 minutes.

1.  **Create a Firebase Project:**
    * Go to the [Firebase Console](https://console.firebase.google.com/).
    * Click "Add project", give it a name (e.g., "PC-Clipboard"), and complete the creation steps.
2.  **Get Server Key (`serviceAccountKey.json`):**
    * In your Firebase project, click the **gear icon ⚙️** > **Project settings**.
    * Go to the **Service accounts** tab.
    * Click **"Generate new private key"** and confirm.
    * A JSON file will download. **Rename it to `serviceAccountKey.json`** and place it in your main project folder.
3.  **Create a Realtime Database:**
    * In the left menu, go to **Build > Realtime Database**.
    * Click **"Create database"**.
    * Choose a location and select **"Start in test mode"** (this allows open access for your local devices). Click **Enable**.
    * At the top of the data viewer, you will see the database URL (e.g., `https://your-project-id-default-rtdb.firebaseio.com`). **Copy this URL.**
4.  **Get Client Keys:**
    * Go back to **Project settings > General** tab.
    * Scroll down to "Your apps" and click the **Web icon (`</>`)** to create a web app.
    * Give it a nickname and click **"Register app"**.
    * You will be shown a `firebaseConfig` object. **Copy the key-value pairs from it.**

### 4. Configure the Python Script

1.  Open `transfer_server.py`.
2.  Paste your **Realtime Database URL** into the `DATABASE_URL` variable.
3.  Paste your **client keys** into the `FIREBASE_CONFIG_CLIENT` dictionary.

## Usage

1.  Open a terminal in the project folder.
2.  Run the server:
    ```bash
    python transfer_server.py
    ```
3.  A QR code image (`qr_code.png`) will be generated and should open automatically.
4.  Scan this QR code with your phone's camera to open the web interface.
5.  Use the different tabs to transfer files or use the shared clipboard.

* **To share files:** Simply add or remove files from the `pc_mobile_transfer/sharing` folder. Click the "Refresh List" button on the app to see the changes.

## Troubleshooting

* **Cannot connect from phone:** This is almost always a **firewall issue** on your PC. Your PC's firewall is blocking the incoming connection from your phone. You must create a new "Inbound Rule" to **allow connections on TCP port 5000**.
* **"Firebase configuration is missing or invalid":** This means the keys in the `FIREBASE_CONFIG_CLIENT` dictionary in `transfer_server.py` are incorrect or you haven't set up the Realtime Database correctly. Double-check all keys and make sure your database is in "test mode".
