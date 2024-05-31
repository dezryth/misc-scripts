import requests
import configparser

# Get keys out of person config.ini
config = configparser.ConfigParser()
config.read("config.ini")


# Replace with your personal access token from YNAB
YNAB_ACCESS_TOKEN = config["DEFAULT"]["YNABAccessToken"]
# Replace with your budget ID
BUDGET_ID = config["DEFAULT"]["BudgetID"]

# YNAB API URL
BASE_URL = f'https://api.youneedabudget.com/v1/budgets/{BUDGET_ID}'

# Set up headers with authorization
headers = {
    'Authorization': f'Bearer {YNAB_ACCESS_TOKEN}'
}

def get_categories():
    # API endpoint to get categories
    endpoint = f'{BASE_URL}/categories'

    # Make the request to YNAB API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json()}")

    categories = response.json()['data']['category_groups']
    return categories

def main():
    categories = get_categories()

    # Iterate through category groups and categories to find the Groceries category
    for group in categories:
        for category in group['categories']:
            print(f"Category Name: {category['name']}, Category ID: {category['id']}")

if __name__ == '__main__':
    main()
