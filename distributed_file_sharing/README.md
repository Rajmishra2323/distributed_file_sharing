# Distributed File Sharing System

A Flask-based local network file sharing system matching the supplied architecture.

## Features

- Upload files to `uploads/`
- View all uploaded files
- Download files
- **Search files by filename**
- Multiple clients can access the Flask server over the local network
- Secure filename handling with `secure_filename`
- Duplicate filenames automatically get a timestamp suffix
- 100 MB upload limit
- Responsive UI

## Project structure

```text
distributed_file_sharing/
├── app.py
├── requirements.txt
├── uploads/
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── files.html
└── static/
    └── style.css
```

## Run on Windows

Open Command Prompt / PowerShell in this folder:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Access from another computer on the same Wi-Fi/LAN

1. Start the server with `python app.py`.
2. Find the server computer's IPv4 address using `ipconfig`.
3. On another device open:

```text
http://SERVER_IP:5000
```

Example:

```text
http://192.168.1.10:5000
```

If Windows Firewall asks, allow Python for your private network.

## File Search

On the Files page, enter part of a filename in the search box.

Examples:

- `report`
- `pdf`
- `project`
- `image.jpg`

The search is case-insensitive and matches partial filenames.

## Important security note

This version follows the supplied architecture and intentionally has **no login/authentication layer**. Anyone who can reach the Flask server can see/download files exposed by the Files page.

For an internet-facing deployment, add authentication, authorization, HTTPS, and per-user file permissions before using it for private files.
