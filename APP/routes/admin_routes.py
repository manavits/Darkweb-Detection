from flask import Blueprint, render_template, request, jsonify, redirect, url_for, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import DarkWebThreat, User
from app import db
from datetime import datetime
import csv
import io
import requests
from bs4 import BeautifulSoup

admin = Blueprint('admin', __name__)

# --------------------------
# DASHBOARD VIEW
# --------------------------
@admin.route('/dashboard', methods=['GET'])
@jwt_required()  # ✅ Require valid JWT token
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('auth.login'))

    token = request.cookies.get('access_token')
    return render_template('admin/dashboard.html', token=token, user_id=user_id)


# --------------------------
# DASHBOARD DATA ENDPOINT
# --------------------------
@admin.route('/dashboard-data', methods=['GET'])
@jwt_required()
def dashboard_data():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = DarkWebThreat.query

    if search:
        query = query.filter(DarkWebThreat.threat_description.ilike(f"%{search}%"))

    threats = query.order_by(DarkWebThreat.timestamp.desc()).paginate(page, per_page, False)

    data = [{
        "url": t.url,
        "description": t.threat_description,
        "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for t in threats.items]

    return jsonify({
        'data': data,
        'total': threats.total,
        'pages': threats.pages,
        'current_page': threats.page
    })


# --------------------------
# SCAN TOR LINK
# --------------------------
@admin.route('/scan', methods=['POST'])
@jwt_required()
def scan_tor_link():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url or not url.endswith('.onion'):
        return jsonify({"error": "Invalid or missing TOR link."}), 400

    keywords = ["illegal", "black market", "hacking", "drugs", "guns", "exploit"]
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=25)

        if response.status_code != 200:
            return jsonify({"error": f"Unable to reach site. Status code: {response.status_code}"}), 502

        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        found_keywords = [kw for kw in keywords if kw.lower() in text_content.lower()]

        if found_keywords:
            threat = DarkWebThreat(
                url=url,
                threat_description=f"Keywords found: {', '.join(found_keywords)}",
                timestamp=datetime.utcnow()
            )
            db.session.add(threat)
            db.session.commit()
            return jsonify({"message": f"Threat detected: {', '.join(found_keywords)}"}), 200

        return jsonify({"message": "No threats found on this TOR link."}), 200

    except requests.exceptions.RequestException as req_err:
        print(f"[TOR SCAN ERROR]: {req_err}")
        return jsonify({"error": "Failed to scan TOR site. Check if Tor proxy is running."}), 504
    except Exception as e:
        print(f"[UNEXPECTED SCAN ERROR]: {e}")
        return jsonify({"error": "Unexpected error during scan."}), 500


# --------------------------
# EXPORT THREAT DATA TO CSV
# --------------------------
@admin.route('/download-csv', methods=['GET'])
@jwt_required()
def export_data():
    threats = DarkWebThreat.query.order_by(DarkWebThreat.timestamp.desc()).all()

    if not threats:
        return Response(
            "No threats found.",
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=darkweb_threats_export.csv"}
        )

    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['URL', 'Description', 'Timestamp'])

    for threat in threats:
        writer.writerow([
            threat.url,
            threat.threat_description,
            threat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=darkweb_threats_export.csv"
        }
    )

