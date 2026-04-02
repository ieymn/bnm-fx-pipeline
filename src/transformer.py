import pandas as pd


def transform_exchange_rate(data):
    """
     Flattens the nested exchange rate JSON from BNM API
    into a clean pandas DataFrame.

    Args:
        data (list): Raw list of currency records from extractor

    Returns:
        DataFrame: Flat table with columns date, currency_code,
                   unit, buying_rate, selling_rate, middle_rate
    """
    records = []

    for item in data:
        records.append({
            "date"         : item["rate"]["date"],
            "currency_code": item["currency_code"],
            "unit"         : item["unit"],
            "buying_rate"  : item["rate"]["buying_rate"],
            "selling_rate" : item["rate"]["selling_rate"],
            "middle_rate"  : item["rate"]["middle_rate"]
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df


def transform_opr(data):
    """
    Transforms flat OPR JSON from BNM API into a pandas DataFrame.

    Args:
        data (dict): Single flat dictionary containing OPR records from extractor

    Returns:
        DataFrame: Single row table with columns year, date,
                   change_in_opr, new_opr_level
    """
    df = pd.DataFrame([data])
    df["date"] = pd.to_datetime(df["date"])
    return df


def transform_interest_rate(data):
    """
    Transform flat interest rate JSON from BNM API into pandas DataFrame

    Args:
        data (dict): Single flat dictionarry containing Interest rate records from extractor

    Return:
        DataFrame: Single row table with column date, overnight, 1_week,
                    1_month, 3_month, 6_month, 1_year
    """

    df = pd.DataFrame([data])
    df["date"] = pd.to_datetime(df["date"])
    return df


def transform_interbank_swap(data):
    """
     Transform flat interbank swap JSON from BNM API into pandas DataFrame

    Args:
        data (dict): Single flat dictionarry containing Interbank swap record from extractor

    Return:
        DataFrame: Single row table with column date, overnight, 1_week, 2_week, 1_month,
                    2_month, 3_month, 6_month, 9_month, 12_month, more_1_year
    """

    df = pd.DataFrame([data])
    df["date"] = pd.to_datetime(df["date"])
    return df


def transform_kijang_emas(data):
    """
     Flattens the nested kijang emas JSON from BNM API
    into a clean pandas DataFrame.

    Args:
        data (dict): Raw list of gold records from extractor

    Returns:
        DataFrame: Flat table with column date, weight,
                    buying, selling
    """

    records = []

    records.append({
        "date"        : data["effective_date"],
        "weight"      : "one_oz",
        "buying"      : data["one_oz"]["buying"],
        "selling"     : data["one_oz"]["selling"]
    })
    
    records.append({
        "date"        : data["effective_date"],
        "weight"      : "half_oz",
        "buying"      : data["half_oz"]["buying"],
        "selling"     : data["half_oz"]["selling"]
    })
    
    records.append({
        "date"        : data["effective_date"],
        "weight"      : "quarter_oz",
        "buying"      : data["quarter_oz"]["buying"],
        "selling"     : data["quarter_oz"]["selling"]
    })
    
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df

if __name__ == "__main__":
    from extractor import run
    raw = run()
    print(transform_exchange_rate(raw["exchange_rate"]))
    print(transform_opr(raw["opr"]))
    print(transform_interest_rate(raw["interest_rate"]))
    print(transform_interbank_swap(raw["interbank_swap"]))
    print(transform_kijang_emas(raw["kijang_emas"]))