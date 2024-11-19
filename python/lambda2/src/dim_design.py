from datetime import datetime
from pprint import pprint

def dim_design(s3):
    timestamp = datetime.now()
    bucket_name = "nc-terraformers-ingestion"
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
    bucket_files = [file["Key"] for file in response['Contents']]
    most_recent = max(bucket_files)
    print(bucket_files, most_recent)
    
