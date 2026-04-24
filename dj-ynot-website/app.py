import os
import re
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_PATTERN = re.compile(r"^[\d\s+()\-]{7,20}$")
MAX_FIELD_LENGTH = 2000


@app.get("/")
def index():
    return render_template("index.html", current_year=datetime.utcnow().year)


def sanitize_text(value: str) -> str:
    if value is None:
        return ""
    value = str(value).replace("\x00", "").strip()
    value = re.sub(r"\s+", " ", value)
    return value[:MAX_FIELD_LENGTH]


def validate_payload(payload: dict) -> tuple[bool, str, dict]:
    required_fields = {
        "fullName": "Full name is required.",
        "email": "Email address is required.",
        "message": "Please share details about your event.",
        "preferredService": "Please select a preferred service.",
        "preferredContactMethod": "Please choose a preferred contact method.",
    }

    cleaned = {k: sanitize_text(v) for k, v in payload.items()}

    honeypot = cleaned.get("website", "")
    if honeypot:
        return False, "Spam submission rejected.", {}

    for field, error_message in required_fields.items():
        if not cleaned.get(field):
            return False, error_message, {}

    email = cleaned.get("email", "")
    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address.", {}

    phone = cleaned.get("phone", "")
    if phone and not PHONE_PATTERN.match(phone):
        return False, "Please enter a valid phone number.", {}

    event_date = cleaned.get("eventDate", "")
    if event_date:
        try:
            datetime.strptime(event_date, "%Y-%m-%d")
        except ValueError:
            return False, "Event date must use YYYY-MM-DD format.", {}

    return True, "", cleaned


def forward_to_freeform(payload: dict) -> tuple[bool, str]:
    """
    Forward contact payload to FREEFORM.

    Configuration:
    - Set FREEFORM_ENDPOINT to your FREEFORM submission URL.
    - Optionally set FREEFORM_API_KEY if your FREEFORM setup requires auth.
    - CONTACT_FORM_RECIPIENT defaults to djynotlive@iCloud.com.
    """
    endpoint = os.getenv("FREEFORM_ENDPOINT", "").strip()
    api_key = os.getenv("FREEFORM_API_KEY", "").strip()
    recipient = os.getenv("CONTACT_FORM_RECIPIENT", "djynotlive@iCloud.com").strip()

    if not endpoint:
        return False, (
            "FREEFORM endpoint is not configured. Set FREEFORM_ENDPOINT in your environment "
            "to enable form forwarding."
        )

    outbound_payload = {
        **payload,
        "recipient": recipient,
        "source": "djynot.live contact form",
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.post(
            endpoint,
            json=outbound_payload,
            headers=headers,
            timeout=12,
        )

        if 200 <= response.status_code < 300:
            return True, "Forwarded successfully."

        return False, (
            "FREEFORM rejected the request "
            f"(status {response.status_code}): {response.text[:200]}"
        )
    except requests.RequestException as exc:
        return False, f"FREEFORM request failed: {exc}"


@app.post("/api/contact")
def api_contact():
    if not request.is_json:
        return jsonify({"success": False, "message": "Expected JSON request body."}), 400

    payload = request.get_json(silent=True) or {}
    is_valid, validation_message, cleaned_payload = validate_payload(payload)

    if not is_valid:
        status = 400 if validation_message != "Spam submission rejected." else 200
        return jsonify({"success": False, "message": validation_message}), status

    forwarded, forward_message = forward_to_freeform(cleaned_payload)

    if not forwarded:
        return (
            jsonify(
                {
                    "success": False,
                    "message": (
                        "We couldn't send your request right now. "
                        "Please email djynot@iCloud.com or call 415-506-9668."
                    ),
                    "developerMessage": forward_message,
                }
            ),
            502,
        )

    return jsonify({"success": True, "message": "Booking request sent successfully."}), 200


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
