import requests
import json
from datetime import datetime
import sys

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"{Colors.BOLD}{Colors.HEADER}💱 REAL-TIME CURRENCY CONVERTER 💱{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def get_exchange_rates():
    
    try:
        print(f"{Colors.BLUE}🔄 Fetching latest exchange rates...{Colors.END}")
        
        # Using exchangerate-api.com free tierr
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and 'rates' in data:
            print(f"{Colors.GREEN}✓ Exchange rates updated successfully!{Colors.END}")
            print(f"{Colors.CYAN}Last updated: {data.get('date', 'N/A')}{Colors.END}\n")
            return data['rates']
        else:
            print(f"{Colors.FAIL}✗ Error: Invalid response format{Colors.END}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}✗ Network Error: {e}{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error: {e}{Colors.END}")
        return None

def display_popular_currencies(rates):
    """displayed popular curencis"""
    popular = {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'INR': 'Indian Rupee',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'AED': 'UAE Dirham'
    }
    
    print(f"{Colors.BOLD}Popular Currencies (1 USD = ):{Colors.END}")
    print(f"{Colors.CYAN}{'-'*50}{Colors.END}")
    
    for code, name in popular.items():
        if code in rates:
            rate = rates[code]
            print(f"{Colors.GREEN}{code:4}{Colors.END} - {name:20} : {Colors.BOLD}{rate:>12.4f}{Colors.END}")
    print(f"{Colors.CYAN}{'-'*50}{Colors.END}\n")

def get_valid_currency(rates, prompt_text):
    
    while True:
        currency = input(f"{Colors.BOLD}{prompt_text}{Colors.END}").upper().strip()
        
        if currency == 'LIST':
            print(f"\n{Colors.CYAN}Available currencies:{Colors.END}")
            currencies = sorted(rates.keys())
            for i in range(0, len(currencies), 6):
                print("  ".join(f"{Colors.GREEN}{c:4}{Colors.END}" for c in currencies[i:i+6]))
            print()
            continue
            
        if currency in rates:
            return currency
        else:
            print(f"{Colors.FAIL}✗ Invalid currency code. Type 'LIST' to see all available currencies.{Colors.END}")

def get_valid_amount():
    
    while True:
        try:
            amount = input(f"{Colors.BOLD}Enter amount: {Colors.END}").strip()
            amount = float(amount)
            
            if amount <= 0:
                print(f"{Colors.FAIL}✗ Amount must be greater than 0{Colors.END}")
                continue
                
            return amount
            
        except ValueError:
            print(f"{Colors.FAIL}✗ Invalid amount. Please enter a number.{Colors.END}")

def convert_currency(amount, from_curr, to_curr, rates):
   
    # Convert to USD first, then to target currency
    if from_curr == 'USD':
        usd_amount = amount
    else:
        usd_amount = amount / rates[from_curr]
    
    
    if to_curr == 'USD':
        result = usd_amount
    else:
        result = usd_amount * rates[to_curr]
    
    return result

def display_conversion_result(amount, from_curr, to_curr, result):
   
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}CONVERSION RESULT:{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    print(f"\n{Colors.GREEN}{amount:,.2f} {from_curr}{Colors.END} = {Colors.BOLD}{Colors.HEADER}{result:,.2f} {to_curr}{Colors.END}\n")
    
    # Show exchange rate
    if from_curr != to_curr:
        rate = result / amount
        print(f"{Colors.CYAN}Exchange Rate: 1 {from_curr} = {rate:.6f} {to_curr}{Colors.END}")
    
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def main():
    
    print_banner()
    rates = get_exchange_rates()
    
    if not rates:
        print(f"{Colors.FAIL}Failed to fetch exchange rates. Please check your internet connection.{Colors.END}")
        return
    
    
    display_popular_currencies(rates)
    
    while True:
        try:
           
            print(f"{Colors.BOLD}New Conversion (or type 'quit' to exit):{Colors.END}")
            print(f"{Colors.CYAN}Tip: Type 'LIST' when entering currency to see all available currencies{Colors.END}\n")
            
            from_curr = get_valid_currency(rates, "From Currency (e.g., USD): ")
            to_curr = get_valid_currency(rates, "To Currency (e.g., EUR): ")
            amount = get_valid_amount()
            
            
            result = convert_currency(amount, from_curr, to_curr, rates)
            
            display_conversion_result(amount, from_curr, to_curr, result)
            
            choice = input(f"{Colors.BOLD}Convert another? (yes/no): {Colors.END}").lower().strip()
            if choice not in ['yes', 'y', '']:
                break
                
            print("\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Conversion cancelled by user.{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}✗ An error occurred: {e}{Colors.END}")
            continue
    
    print(f"\n{Colors.GREEN}Thank you for using Currency Converter! 👋{Colors.END}\n")

if __name__ == "__main__":
    main()