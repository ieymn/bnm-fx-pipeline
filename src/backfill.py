import requests
import pandas as pd
import time
from datetime import date, timedelta


BASE_URL   = "https://api.bnm.gov.my/public"
HEADERS    = {"Accept": "application/vnd.BNM.API.v1+json"}
START_DATE = date(2025, 1, 1)
END_DATE   = date.today()

DATE_ENDPOINTS = {
    "interbank_swap" : "/interbank-swap/date/",
    "interest_rate"  : "/interest-rate/date/",
    "kijang_emas"    : "/kijang-emas/date/"
}

YEAR_ENDPOINTS = {
    "opr" : "/opr/year/"
}


def fetch_endpoint(endpoint):
    """
    Fetches a single BNM API endpoint and returns raw JSON response.

    Args:
        endpoint (str): API endpoint path

    Returns:
        dict: Raw JSON response from BNM API
    """
    url = BASE_URL + endpoint
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_by_date():
    """
    Loops through all dates from START_DATE to END_DATE
    and fetches data for each date endpoint.

    Args:
        None

    Returns:
        dict: Dictionary of lists, one list per endpoint
    """
    all_data = {name: [] for name in DATE_ENDPOINTS}
    current_date = START_DATE

    while current_date <= END_DATE:
        date_str = current_date.strftime("%Y-%m-%d")

        for name, endpoint in DATE_ENDPOINTS.items():
            try:
                response = fetch_endpoint(endpoint + date_str)
                all_data[name].append(response["data"])
            except Exception as e:
                print(f"Skipping {name} on {date_str}: {e}")

        time.sleep(0.5)
        current_date += timedelta(days=1)

    return all_data


def fetch_by_year():
    """
    Loops through all years from START_DATE year to END_DATE year
    and fetches data for each year endpoint.

    Args:
        None

    Returns:
        dict: Dictionary of lists, one list per endpoint
    """
    all_data = {name: [] for name in YEAR_ENDPOINTS}
    start_year = START_DATE.year
    end_year   = END_DATE.year

    for year in range(start_year, end_year + 1):
        for name, endpoint in YEAR_ENDPOINTS.items():
            try:
                response = fetch_endpoint(endpoint + str(year))
                records  = response["data"]
                if isinstance(records, list):
                    all_data[name].extend(records)
                else:
                    all_data[name].append(records)
            except Exception as e:
                print(f"Skipping {name} for {year}: {e}")

    return all_data


def run():
    """
    Runs the full backfill — fetches all historical data
    by date and by year.

    Args:
        None

    Returns:
        dict: Combined dictionary of all historical data
    """
    print(f"Starting backfill from {START_DATE} to {END_DATE}...")

    date_data = fetch_by_date()
    year_data = fetch_by_year()

    all_data = {**date_data, **year_data}

    print("Backfill extraction complete.")
    return all_data


#if __name__ == "__main__":
    run()

if __name__ == "__main__":
    from transformer import (
        transform_interest_rate,
        transform_interbank_swap,
        transform_kijang_emas,
        transform_opr
    )
    from loader import load

    raw = run()

    all_data = {
    "interest_rate" : pd.concat([pd.DataFrame([r]) for r in raw["interest_rate"] if r], ignore_index=True),
    "interbank_swap": pd.concat([pd.DataFrame([r]) for r in raw["interbank_swap"] if r], ignore_index=True),
    "kijang_emas"   : pd.concat([transform_kijang_emas(r) for r in raw["kijang_emas"] if r], ignore_index=True),
    "opr"           : pd.DataFrame(raw["opr"] if raw["opr"] else [])
}

    load(all_data)