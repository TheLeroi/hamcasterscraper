from hamscraper import hamcaster_scraper
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_number', methods=['GET'])
def process_number():
    # Get the 'number' parameter from the query string
    number = request.args.get('number', type=str)
    
    if number is None:
        return jsonify({"error": "Missing 'number' parameter"}), 400
    
    def is_not_numeric(s):
        return not s.isdigit()

    if is_not_numeric(number):
        return jsonify({"error":"your fid is invalid make sure to enter a valid numric fid id! "})
    
    # Create a response JSON
    response = hamcaster_scraper(number)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
