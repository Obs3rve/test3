from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Validate input
def validate(number):
    print(f"📌 Raw input: {number}")  # Debugging log

    if not number:
        raise ValueError("Missing 'number' parameter")

    try:
        number = float(number)  # Convert to float first
        number = int(number)  # Convert to integer after
        print(f"✔ Converted number: {number}")  # Debugging log
    except ValueError:
        print("❌ Error: Invalid input")
        raise ValueError("Invalid input, must be a valid number")

    return number


# Check if prime
def is_prime(number):
    if number < 2:
        return False
    for x in range(2, (number // 2) + 1):
        if number % x == 0:
            return False
    return True

# Check if Armstrong number
def is_armstrong(number):
    order = len(str(abs(number)))  # Handle negative numbers
    sum_total = sum(int(digit) ** order for digit in str(abs(number)))
    return abs(number) == sum_total

# Check if perfect number
def is_perfect(number):
    if number <= 0:
        return False
    return sum(x for x in range(1, number) if number % x == 0) == number

# Calculate sum of digits
def calc_sum(number):
    return sum(int(digit) for digit in str(abs(number)))

# Get fun fact
def get_fun_fact(number):
    url = f"http://numbersapi.com/{number}/math"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to retrieve data. Status code: {response.status_code}"
    
    return response.text

# Get properties
def get_properties(number):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")
    return properties

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number')

    try:
        number = validate(number_param)
    except ValueError as e:
        return jsonify({"error": True, "message": str(e)}), 400

    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": get_properties(number),
        "digit_sum": calc_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response_data), 200

if __name__ == '__main__':
    # Run the app on a publicly accessible address
    app.run(debug=True, host='0.0.0.0', port=5000)
