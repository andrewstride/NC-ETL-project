from io import BytesIO, StringIO
import logging
import pandas as pd
import boto3


def convert_to_parquet(star_schema_df):
    
   

    out_buffer = BytesIO()
    star_schema_df.to_parquet(out_buffer, index=False)

    return out_buffer.getvalue()