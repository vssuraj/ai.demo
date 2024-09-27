from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database of country information
country_info = {
    "US": {"name": "United States", "currency": "USD", "compliance_rules": ["No transaction via NR", "Rule2"]},
    "CA": {"name": "Canada", "currency": "CAD", "compliance_rules": ["Rule3", "Rule4"]},
    "GB": {"name": "United Kingdom", "currency": "GBP", "compliance_rules": ["Rule5", "Rule6"]},
    "IR": {"name": "Iran", "currency": "IRR", "compliance_rules": ["Block all transactions to and from Iran"]},
    "EU": {"name": "European Union", "currency": "EUR", "compliance_rules": ["Rule7", "Rule8"]}
}

@app.route('/country/<code>', methods=['GET'])
def get_country_info(code):
    info = country_info.get(code.upper())
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Country code not found"}), 404

@app.route('/transaction', methods=['POST'])
def handle_transaction():
    data = request.json
    from_country = data.get('from_country')
    to_country = data.get('to_country')
    amount = data.get('amount')
    currency = data.get('currency')

    if not from_country or not to_country or not amount or not currency:
        return jsonify({"error": "Missing transaction details"}), 400

    from_info = country_info.get(from_country.upper())
    to_info = country_info.get(to_country.upper())

    if not from_info or not to_info:
        return jsonify({"error": "Invalid country code"}), 404

    if currency not in ["USD", "EUR", "GBP"]:
        return jsonify({"error": "Unsupported currency"}), 400

    if "Block all transactions to and from Iran" in from_info["compliance_rules"] or "Block all transactions to and from Iran" in to_info["compliance_rules"]:
        return jsonify({"error": "Transactions to or from Iran are blocked"}), 403

    return jsonify({"status": "Transaction approved", "amount": amount, "currency": currency}), 200

if __name__ == '__main__':
    app.run(port=5000)
