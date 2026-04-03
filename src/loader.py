import sqlite3
import pandas as pd
import os

DB_PATH = "data/bnm.db"

def get_connection():
    """
    Create a data folder if it doesn't exist and
    return a SQLite database connection

    Args:
        None

    Return:
        Connection: SQLite connection database
    """

    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def load_table(conn, df, table_name):
    """
    Loads a pandas DataFrame into a SQLite table.
    If the table already exists, appends new rows.

    Args:
        conn (connection): SQLite connection object
        df (DataFrame): Clean DataFrame from transformer
        table_name (str): Name of the target table in SQLite

    Returns:
        None
    """
    df.to_sql(table_name, conn, if_exists = "append", index = False)
    print(f'Loaded {len(df)} rows into {table_name}') 

    
def load(all_data):
    """
    Loads all transformed DataFrames into SQLite.

    Args:
        all_data (dict): Dictionary of DataFrames from transformer

    Returns:
        None
    """
    conn = get_connection()

    for table_name, df in all_data.items():
        load_table(conn, df, table_name)

    conn.close()
    print("All Table Loaded")


if __name__ == "__main__":
    from extractor import run as extract
    from transformer import (
        transform_exchange_rate,
        transform_interest_rate,
        transform_interbank_swap,
        transform_opr,
        transform_kijang_emas
    )

    raw = extract()

    all_data = {
        "exchange_rate" : transform_exchange_rate(raw["exchange_rate"]),
        "interest_rate" : transform_interest_rate(raw["interest_rate"]),
        "interbank_swap": transform_interbank_swap(raw["interbank_swap"]),
        "opr"           : transform_opr(raw["opr"]),
        "kijang_emas"   : transform_kijang_emas(raw["kijang_emas"])
    }
    
    load(all_data)