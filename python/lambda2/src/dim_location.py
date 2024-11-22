import pandas as pd
import logging

def dim_location(address_df):
    if isinstance(address_df, pd.DataFrame):
        try:
            new_df = address_df[["address_id",
                                "address_line_1",
                                "address_line_2",
                                "district",
                                "city",
                                "postal_code",
                                "country",
                                "phone"]].copy()
            new_df.drop_duplicates()
            new_df = new_df.rename(columns={"address_id": "location_id"})
            return new_df
        except Exception as e:
            logging.error(e)
    else:
        logging.error("Given paramater should be a DataFrame.")
    return {"result": "Failure"}
