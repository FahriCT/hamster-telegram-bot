import sys
import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style

init(autoreset=True)

auto_claim_daily_combo = None
combo_list = []

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'authorization' : 'authToken is empty, store token null',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['authToken']
        elif response.status_code == 403:
            print(Fore.RED + Style.BRIGHT + "\rAkses Ditolak. Status 403", flush=True)
        elif response.status_code == 500:
            print(Fore.RED + Style.BRIGHT + "\rInternal Server Error", flush=True)
        else:
            error_data = response.json()
            if "invalid" in error_data.get("error_code", "").lower():
                print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Data init tidak valid", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rGagal Mendapatkan Token. {error_data}", flush=True)
    except requests.exceptions.Timeout:
        print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Request Timeout", flush=True)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + Style.BRIGHT + "\rGagal Mendapatkan Token. Kesalahan Koneksi", flush=True)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\rGagal Mendapatkan Token. Error: {str(e)}", flush=True)
    return None

def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def main(query_id):
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Starting Hamster Kombat....\n\n")

    token_dict = {}  # Dictionary to store successful tokens
    token = token_dict.get(query_id)
    
    if token:
        print(Fore.GREEN + Style.BRIGHT + f"\n\n\rMenggunakan token yang sudah ada...", end="", flush=True)
    else:
        print(Fore.GREEN + Style.BRIGHT + f"\n\n\rMendapatkan token...              ", end="", flush=True)
        token = get_token(query_id)
        if token:
            token_dict[query_id] = token
            print(Fore.GREEN + Style.BRIGHT + f"\n\n\rBerhasil mendapatkan token    ", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\n\n\rGagal mendapatkan token\n\n", flush=True)
            return  # Keluar jika gagal mendapatkan token

    response = authenticate(token)
    
    ## TOKEN AMAN
    if response.status_code == 200:
        user_data = response.json()
        username = user_data.get('telegramUser', {}).get('username', 'Username Kosong')
        firstname = user_data.get('telegramUser', {}).get('firstName', 'Kosong')
        lastname = user_data.get('telegramUser', {}).get('lastName', 'Kosong')
        
        print(Fore.GREEN + Style.BRIGHT + f"\r\n======[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]======")

        # Sync Clicker
        print(Fore.GREEN + f"\rGetting info user...", end="", flush=True)
        response = sync_clicker(token)
        if response.status_code == 200:
            clicker_data = response.json()['clickerUser']
            print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level ] : {clicker_data['level']}          ", flush=True)
            print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned ] : {int(clicker_data['totalCoins'])}")
            print(Fore.YELLOW + Style.BRIGHT + f"[ Coin ] : {int(clicker_data['balanceCoins'])}")
            print(Fore.YELLOW + Style.BRIGHT + f"[ Energy ] : {clicker_data['availableTaps']}")
            boosts = clicker_data['boosts']
            boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
            boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
            
            print(Fore.CYAN + Style.BRIGHT + f"[ Level Energy ] : {boost_max_taps_level}")
            print(Fore.CYAN + Style.BRIGHT + f"[ Level Tap ] : {boost_earn_per_tap_level}")
            print(Fore.CYAN + Style.BRIGHT + f"[ Exchange ] : {clicker_data['exchangeId']}")
            if clicker_data['exchangeId'] == None:
                print(Fore.GREEN + '\rSeting exchange to OKX..', end="", flush=True)
                exchange_set = exchange(token)
                if exchange_set.status_code == 200:
                    print(Fore.GREEN + Style.BRIGHT + '\rSukses set exchange ke OKX', flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + '\rGagal set exchange', flush=True)
            print(Fore.CYAN + Style.BRIGHT + f"[ Passive Earn ] : {clicker_data['earnPassivePerHour']}\n")
            
    ## TOKEN MATI        
    elif response.status_code == 401:
        error_data = response.json()
        if error_data.get("error_code") == "NotFound_Session":
            print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
            token_dict.pop(query_id, None)  # Remove invalid token
        else:
            print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
    else:
        print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")

    time.sleep(1)

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Hamster Kombat BOT!")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/adearman/hamsterkombat")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hamster.py [query_id]")
        sys.exit(1)

    query_id = sys.argv[1]
    main(query_id)
