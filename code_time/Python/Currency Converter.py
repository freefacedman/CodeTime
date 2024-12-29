#pip install requests
import sys
import requests

def get_rates():
    url = "https://api.exchangerate.host/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    
    data = response.json()
    
    if not data.get('success', False):
        print("API request was not successful.")
        print(data.get('error', 'No error message provided.'))
        sys.exit(1)
    
    rates = data.get('rates')
    if not rates:
        print("Unexpected response format: 'rates' key not found.")
        print(data)
        sys.exit(1)
    
    return rates

def convert(amount, from_currency, to_currency, rates):
    try:
        converted_amount = amount / rates[from_currency] * rates[to_currency]
    except KeyError as e:
        print(f"Currency code not found: {e}")
        sys.exit(1)
    return converted_amount

def main():
    rates = get_rates()
    
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount entered.")
        sys.exit(1)
    
    from_currency = input("From currency (e.g., USD): ").upper()
    to_currency = input("To currency (e.g., EUR): ").upper()
    
    if from_currency not in rates:
        print(f"Invalid from currency code: {from_currency}")
        sys.exit(1)
    
    if to_currency not in rates:
        print(f"Invalid to currency code: {to_currency}")
        sys.exit(1)
    
    result = convert(amount, from_currency, to_currency, rates)
    print(f"{amount} {from_currency} = {result:.2f} {to_currency}")

if __name__ == "__main__":
    main()
