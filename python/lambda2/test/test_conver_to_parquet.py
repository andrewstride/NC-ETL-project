from src.convert_to_parquet import convert_to_parquet
from testconf import processing_bucket, ingestion_bucket
import pandas as pd
from io import BytesIO
def test_output_is_parq():
    
    data = [['a1', 'b1'], ['a2', 'b3'], ['a3', 'b3']]

    df = pd.DataFrame(data, columns=['col1', 'col2'])
    output = convert_to_parquet(df)
    print(output)
    assert pd.read_parquet(output) is not None
