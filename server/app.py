from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_daraz

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"success": False, "message": "Query parameter is required"}), 400

    try:
        products = scrape_daraz(query)
        return jsonify({"success": True, "data": products})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
