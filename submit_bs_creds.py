"""
This script was originally written to sabotage scammers
attempting to phish for credentials of bank members.
I've modified it slightly, removing the specific URL.
Not to protect them, but to protect myself.
Please feel free to adapt it to your needs to sabotage
any scammers you come across.
"""

import time
import random
import string
import requests
import names

# Specify the URL of the telegram API URL of the scammer below:
SCAMMER_URL = 'https://api.telegram.org/bot1487410171:AAF60BxHlwByxSyBzI88bi2IRFU5C6P71r4/' \
    'sendMessage?chat_id=-748374456&text='

TEXT = ['BankWestLogs', 'BOALogs', 'CapitalOneLogs', 'HSBCLogs', 'NavyFederalLogs', \
    'PNCLogs', 'USBankLogs', 'USAALogs', 'CitiLogs', 'SuntrustLogs']


def random_string_generator(str_size, allowed_chars):
    """Generates a random string of a specified size with allowed characters."""
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


def random_username_generator():
    """Generates a random username with a 50% of male or female name and""" \
    """two-digit int between 60 and 99"""
    if random.random() < .5:
        rand_name = names.get_first_name(gender='male')
    else:
        rand_name = names.get_first_name(gender='female')

    rand_name += str(random.randint(60, 99))
    return rand_name


usernamechars = string.ascii_letters + string.digits
passwordchars = string.ascii_letters + string.punctuation
size = random.randint(8, 12)


while True:
    try:
        x = requests.get(SCAMMER_URL + random.choice(TEXT) + '==' + random_username_generator() +
                         '=' + random_string_generator(size, passwordchars))
        print(str(x.json()['result']['message_id']) +
              ' - ' + x.json()['result']['text'])
        time.sleep(20)
    except Exception:
        pass
