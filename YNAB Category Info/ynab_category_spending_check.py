import requests
import datetime
import configparser
import chump

# Get keys out of personal config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Use pushover?
pushover_enabled = config["DEFAULT"].getboolean("UsePushover", True)

# Replace with your personal access token from YNAB
YNAB_ACCESS_TOKEN = config["DEFAULT"]["YNABAccessToken"]
# Replace with your budget ID
BUDGET_ID = config["DEFAULT"]["BudgetID"]
# Replace with your Groceries category ID
GROCERIES_CATEGORY_ID = config["CategoryIDs"]["Groceries"]

# Threshold for spending
THRESHOLD = 6000

# YNAB API URL
BASE_URL = f'https://api.youneedabudget.com/v1/budgets/{BUDGET_ID}'

# Set up headers with authorization
headers = {
    'Authorization': f'Bearer {YNAB_ACCESS_TOKEN}'
}

def get_transactions():
    # Get the current year
    current_year = datetime.datetime.now().year

    # API endpoint to get transactions
    endpoint = f'{BASE_URL}/transactions?since_date={current_year}-01-01'

    # Make the request to YNAB API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json()}")

    transactions = response.json()['data']['transactions']
    return transactions

def calculate_groceries_spent(transactions):
    total_spent = 0
    for transaction in transactions:
        if transaction['category_id'] == GROCERIES_CATEGORY_ID:
            total_spent += transaction['amount']

    # YNAB amounts are in milliunits, so divide by 1000 to get the actual amount
    total_spent = total_spent / 1000
    return total_spent

def send_pushover_message(message, title):
    pushover_token = config["DEFAULT"]["PushoverToken"]
    pushover_user_key = config["DEFAULT"]["PushoverUserKey"]
    
    app = chump.Application(pushover_token)
    user = app.get_user(pushover_user_key)
    user.send_message(message, title=title)

def main():
    transactions = get_transactions()
    total_groceries_spent = calculate_groceries_spent(transactions)
    print(f"Total spent on groceries in the current year: ${total_groceries_spent*-1:.2f}")

    if pushover_enabled and total_groceries_spent*-1 > THRESHOLD:
        message = f"Spending on groceries has exceeded ${THRESHOLD}. Total spent: ${total_groceries_spent*-1:.2f}"
        try:
            send_pushover_message(message, "YNAB Grocery Spending Surpasses Threshold")
        except Exception as e:
            print(f"Error sending Pushover notification: {e}")

if __name__ == '__main__':
    main()