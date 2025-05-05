from flask import Blueprint, jsonify, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.darkweb_scanner import scan_tor_sites  # Ensure this function is implemented in darkweb_scanner.py

# Create a Blueprint for main routes
main = Blueprint('main', __name__)

# Route for the homepage, redirecting to the login page
@main.route('/')
def home():
    return redirect(url_for('auth.login'))  # Redirect to the login route

@main.route('/scan', methods=['POST'])
@jwt_required()
def scan():
    # Get user identity from the JWT token
    user_id = get_jwt_identity()

    # Try to get the request JSON data
    data = request.get_json()

    # Handle case where no data is provided
    if not data:
        return jsonify({"error": "No input provided"}), 400

    # Extract keywords or use default values
    keywords = data.get("keywords", ["password", "leak", "credit card"])

    # Validate that keywords is a list
    if not isinstance(keywords, list):
        return jsonify({"error": "Keywords should be a list"}), 400

    # Ensure that the keywords list is not empty
    if not keywords:
        return jsonify({"error": "Keywords list cannot be empty"}), 400

    try:
        # Log the scan start
        print(f"Starting scan for user {user_id} with keywords: {keywords}")

        # Run the Dark Web scan with the provided keywords
        scan_results = scan_tor_sites(keywords)

        if not scan_results:
            return jsonify({
                "message": "✅ Dark Web Scan Completed, but no threats were found.",
                "scanned_by": user_id,
                "keywords": keywords,
                "scan_results": []  # Empty list if no threats are found
            })

        # If scan results are found
        return jsonify({
            "message": "✅ Dark Web Scan Completed!",
            "scanned_by": user_id,
            "keywords": keywords,
            "scan_results": scan_results  # Include scan results
        })

    except Exception as e:
        # Return a 500 error if scanning fails
        print(f"[SCAN ERROR]: {str(e)}")  # Log the error
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500












