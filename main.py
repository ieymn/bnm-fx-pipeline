
from src.extractor import run as extract
from src.transformer import (
    transform_exchange_rate,
    transform_interest_rate,
    transform_interbank_swap,
    transform_opr,
    transform_kijang_emas
)
from src.loader import load

def main():
    """
    Orchestrates the full BNM ETL pipeline.
    Extract → Transform → Load

    Args:
        None

    Returns:
        None
    """
    print("=" * 50)
    print("BNM Pipeline starting...")
    print("=" * 50)

    # Extract
    raw = extract()

    # Transform
    all_data = {
        "exchange_rate" : transform_exchange_rate(raw["exchange_rate"]),
        "interest_rate" : transform_interest_rate(raw["interest_rate"]),
        "interbank_swap": transform_interbank_swap(raw["interbank_swap"]),
        "opr"           : transform_opr(raw["opr"]),
        "kijang_emas"   : transform_kijang_emas(raw["kijang_emas"])
    }

    # Load
    load(all_data)

    print("=" * 50)
    print("BNM Pipeline complete.")
    print("=" * 50)


if __name__ == "__main__":
    main()