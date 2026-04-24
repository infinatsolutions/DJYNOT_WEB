# DJ YNOT Website

Production-ready Flask website for **DJ YNOT** (https://djynot.live) with premium dark styling, conversion-focused copy, and a FREEFORM-ready contact workflow.

## 1) Project Overview

This site is designed to help visitors quickly understand services, event coverage, and booking options for DJ YNOT. It includes:
- Responsive one-page homepage
- Service, experience, event type, about, and benefit sections
- Contact links (email + phone + site)
- Booking form with client/server validation
- Flask API endpoint for forwarding submissions to FREEFORM

## 2) Tech Stack

- **Backend:** Python + Flask
- **Frontend:** HTML (Flask templates), CSS, Vanilla JavaScript
- **Form forwarding:** Python `requests` to FREEFORM endpoint

## 3) File Structure

```text
dj-ynot-website/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── assets/
│       └── README.md
└── templates/
    └── index.html
```

## 4) Local Setup Instructions

1. Change into the project directory:
   ```bash
   cd dj-ynot-website
   ```
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Create a Python virtual environment and activate it (see below).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open in browser:
   - http://127.0.0.1:5000

## 5) Python Virtual Environment Instructions

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 6) Install Command

```bash
pip install -r requirements.txt
```

## 7) Run Command

```bash
python app.py
```

## 8) Environment Variable Setup

Configure these in `.env`:

- `FREEFORM_ENDPOINT=`
- `FREEFORM_API_KEY=` (optional; only if your FREEFORM setup requires auth)
- `CONTACT_FORM_RECIPIENT=djynotlive@iCloud.com`
- `FLASK_SECRET_KEY=` (set to a secure random value)

## 9) FREEFORM Setup Steps

1. Obtain your FREEFORM submission endpoint URL.
2. Set `FREEFORM_ENDPOINT` in `.env`.
3. If FREEFORM requires authentication, set `FREEFORM_API_KEY`.
4. Keep `CONTACT_FORM_RECIPIENT=djynotlive@iCloud.com`.
5. Submit a test booking request from the website form.
6. Verify request delivery in your FREEFORM destination.

Notes:
- If `FREEFORM_ENDPOINT` is missing, the API returns a helpful developer message.
- API keys are used only server-side and never exposed to frontend JavaScript.

## 10) How to Deploy

### Option A: Any VPS/container
1. Copy project files to server.
2. Create/activate virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env`.
5. Run with a production WSGI server (example):
   ```bash
   gunicorn -w 2 -b 0.0.0.0:5000 app:app
   ```
6. Place behind reverse proxy (Nginx/Caddy) and enable HTTPS.

### Option B: Platform deployment (Render/Railway/Fly/etc.)
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py` (or preferred production command)
- Set environment variables in platform dashboard.

## 11) How to Customize Website Copy

- Edit section text in `templates/index.html`.
- Update SEO metadata in `<head>` of `templates/index.html`.
- Modify brand colors/visual style in `static/css/styles.css`.
- Update interaction behavior in `static/js/main.js`.

## 12) Testing Checklist

- [ ] Home page loads at `/`
- [ ] Mobile menu opens/closes and is keyboard accessible
- [ ] Navigation anchor links scroll correctly
- [ ] Contact links open correct email and phone actions
- [ ] Form blocks empty required fields client-side
- [ ] Form sends JSON payload to `/api/contact`
- [ ] Server validates email and required fields
- [ ] Honeypot submissions are rejected
- [ ] FREEFORM forwarding works with configured endpoint
- [ ] SEO metadata and JSON-LD are present
- [ ] Layout is responsive across mobile/tablet/desktop
- [ ] Reduced-motion preferences are respected
