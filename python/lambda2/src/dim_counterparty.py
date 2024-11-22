import pandas as pd
import logging


def dim_counterparty(counterparty_df, address_df):
    """Takes two DataFrames in counterparty and address
    table format and converts it to star_schema/dim_counterparty format

    Paramaters:
        counterparty_df: a pandas DataFrame
        address_df: a pandas DataFrame

    Returns:
        DataFrame: in dim_counterparty format, if successful
        OR
        Dict (dict): {"result": "Failure"}, if unsuccessful
    """
    if isinstance(counterparty_df, pd.DataFrame) and isinstance(
        address_df, pd.DataFrame
    ):
        try:
            new_df = counterparty_df[
                ["counterparty_id", "counterparty_legal_name"]
            ].copy()

            new_df["counterparty_legal_address_line_1"] = address_df["address_line_1"]
            new_df["counterparty_legal_address_line_2"] = address_df["address_line_2"]
            new_df["counterparty_legal_district"] = address_df["district"]
            new_df["counterparty_legal_city"] = address_df["city"]
            new_df["counterparty_legal_postal_code"] = address_df["postal_code"]
            new_df["counterparty_legal_country"] = address_df["country"]
            new_df["counterparty_phone_number"] = address_df["phone"]
            return new_df
        except Exception as e:
            logging.error(e)
    else:
        logging.error("Given paramater should be a DataFrame.")
    return {"result": "Failure"}
