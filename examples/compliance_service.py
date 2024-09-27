from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database of country information
country_info = {
    "US": {"name": "United States", "currency": "USD", "compliance_rules": ["No transaction via NR", "Rule2"]},
    "CA": {"name": "Canada", "currency": "CAD", "compliance_rules": ["Rule3", "Rule4"]},
    "GB": {"name": "United Kingdom", "currency": "GBP", "compliance_rules": ["Rule5", "Rule6"]},
    "IR": {"name": "Iran", "currency": "IRR", "compliance_rules": ["Block all transactions to and from Iran"]}
}

@app.route('/country/<code>', methods=['GET'])
def get_country_info(code):
    info = country_info.get(code.upper())
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Country code not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)
