import requests
import pandas as pd

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
    """
    Fetches a single BNM API endpoint and returns the raw JSON response.

    Args:
        endpoint (str): API endpoint path e.g. '/opr'

    Returns:
        dict: Raw JSON response from BNM API
    """
    url = BASE_URL + endpoint
    print(f'Fetching {url}')
    response = requests.get(url, headers = HEADERS, timeout = 10)
    response.raise_for_status()
    return response.json()

def run():
    """
    Loops through all BNM endpoints and returns extracted data.

    Args:
        None

    Returns:
        dict: Dictionary of all endpoint data keyed by endpoint name
    """
   
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

