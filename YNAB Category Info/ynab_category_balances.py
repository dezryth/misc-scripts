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

# Category IDs to check
CATEGORY_IDS = list(config["CategoryIDs"].values())

# YNAB API URL
BASE_URL = f'https://api.youneedabudget.com/v1/budgets/{BUDGET_ID}'

# Set up headers with authorization
headers = {
    'Authorization': f'Bearer {YNAB_ACCESS_TOKEN}'
}

def get_category_balances():
    # API endpoint to get categories
    endpoint = f'{BASE_URL}/categories'

    # Make the request to YNAB API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json()}")

    categories = response.json()['data']['category_groups']
    return categories

def filter_balances_by_category(categories):
    balances = {}
    for group in categories:
        for category in group['categories']:
            if category['id'] in CATEGORY_IDS:
                balances[category['name']] = category['balance'] / 1000  # Convert from milliunits
    return balances

def send_pushover_message(message, title):
    pushover_token = config["DEFAULT"]["PushoverToken"]
    pushover_user_key = config["DEFAULT"]["PushoverUserKey"]
    
    app = chump.Application(pushover_token)
    user = app.get_user(pushover_user_key)
    user.send_message(message, title=title)

def main():
    categories = get_category_balances()
    balances = filter_balances_by_category(categories)

    # Get the current date
    current_date = datetime.datetime.now().date()

    # Format the date as mm/dd/yyyy
    formatted_date = current_date.strftime("%m/%d/%Y")

    message = "Available balances:\n"
    for category, balance in balances.items():
        message += f"{category}: ${balance:.2f}\n"

    print(message)

    if pushover_enabled:
        try:
            send_pushover_message(message, f"YNAB Update {formatted_date}")
        except Exception as e:
            print(f"Error sending Pushover notification: {e}")

if __name__ == '__main__':
    main()