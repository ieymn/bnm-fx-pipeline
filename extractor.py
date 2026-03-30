import requests
import pandas as pd
import os
from datetime import datetime

BASE_URL = "https://api.bnm.gov.my/public"

HEADERS  = {"Accept": "application/vnd.BNM.API.v1+json"}

ENDPOINTS = {
    "exchange_rate"  : "/exchange-rate?session=0900&quote=rm",
    "interest_rate"  : "/interest-rate?product=money_market_operations",
    "interbank_swap" : "/interbank-swap",
    "opr"            : "/opr",
    "kijang_emas"    : "/kijang-emas"
}


def fetch_endpoint(endpoint):
    url = BASE_URL + endpoint
    print(f'Fetching {url}')
    response = requests.get(url, headers = HEADERS, timeout = 10)
    response.raise_for_status()
    return response.json()

def run():
    print('Starting Extraction...')
    all_data = {}

    for name, endpoint in ENDPOINTS.items():
        data = fetch_endpoint(endpoint)
        all_data[name] = data["data"]
        print(f"Done: {name}")

    print("Extraction complete.")
    return all_data

if __name__ == "__main__":
    run()