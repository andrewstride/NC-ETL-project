from datetime import datetime
from pprint import pprint
import json
import pandas as pd
from io import BytesIO, StringIO

def dim_design(s3):
    timestamp = datetime.now()
    bucket_name = "nc-terraformers-ingestion"
    processed_bucket = "nc-terraformers-processing"
    # design_id
    # design_name
    # file_location
    # file_name

    ''' Make file1 '''
    with open('file1.txt', 'w', encoding='utf-8') as file:
        file.write("Text of file1!")
        file1_name = 'design/design_2024-11-18 16:53:23.353536.csv'
    s3.upload_file('file1.txt', bucket_name, file1_name)

    ''' Make file2 '''
    with open('file2.txt', 'w', encoding='utf-8') as file:
        file.write("Text of file2!")
        file2_name = 'design/design_2024-11-18 19:15:01.821957.csv'
    s3.upload_file('file2.txt', bucket_name, file2_name)

    ''' Make file3 '''
    with open('file3.txt', 'w', encoding='utf-8') as file:
        file.write("Text of file3!")
        file3_name = 'not a design table!.csv'
    s3.upload_file('file3.txt', bucket_name, file3_name)
   

    response = s3.list_objects_v2(Bucket=bucket_name,
                                  Prefix="design/")
    # bucket_files = [file["Key"] for file in response['Contents']]
    # most_recent = max(bucket_files)
    # print(bucket_files, most_recent)

    response = s3.get_object(Bucket=bucket_name, Key="design_timestamp.json")
    object_content = json.loads(response["Body"].read().decode("utf-8"))
    print(type(object_content))    

    latest_timestamp = object_content["design"]
    print(latest_timestamp)

    latest_file = s3.get_object(Bucket=bucket_name, Key=f"design/design_{latest_timestamp}.csv")
    latest_data = latest_file["Body"].read().decode("utf-8")

    df = pd.read_csv(StringIO(latest_data))

    reformated_df = df[["design_id","design_name","file_location","file_name"]].copy()
    print(reformated_df)
    out_buffer = BytesIO()
    reformated_df.to_parquet(out_buffer,index=False)
    s3.put_object(Bucket=processed_bucket, Body=out_buffer.getvalue(), Key=f"dim_design/dim_design_{timestamp}.parquet")