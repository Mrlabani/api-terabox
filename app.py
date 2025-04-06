from flask import Flask, request, jsonify
from terabox import get_links

app = Flask(__name__)

@app.route('/api/terabox', methods=['GET'])
def terabox_api():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400
    try:
        result = get_links(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
  
