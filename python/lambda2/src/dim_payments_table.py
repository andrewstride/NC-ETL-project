import boto3
import pandas as pd
from io import BytesIO, StringIO
import logging

s3 = boto3.client("s3")

def dim_new_staff(s3):
    try:
        """
        collecting all data from the respective table
        """
        ingestion_bucket = "nc-terraformers-ingestion"
        staff_list = s3.list_objects_v2(
            Bucket=ingestion_bucket,
            Prefix="staff/"
        )["Contents"]

        department_list = s3.list_objects_v2(
            Bucket=ingestion_bucket,
            Prefix="department/"
        )["Contents"]

        """
        As the object_list is list of all csv file,
        using for loop to append all the csv file to append in a single file.
        """

        #get the last timestamp and compare it with existing timestamp
        #if it is not equal then get the new csv file from the corresponding folder.
        #or
        #go to the folder collect all the csv files in a list and looping through append the 
        staff_csv_files = [file["Key"] for file in staff_list if file["Key"].endswith(".csv")]
        department_csv_files = [file["Key"] for file in department_list if file["Key"].endswith(".csv")]

        """
        using StringIO convering the string data in to dataframe and concatinationg into
        a single csv file
        """
        df_staff_list = []
        for key in staff_csv_files:
            staff_obj = s3.get_object(Bucket=ingestion_bucket, Key=key)
            staff_data = staff_obj["Body"].read().decode("utf-8")
            df_staff_list.append(pd.read_csv(StringIO(staff_data)))
        df_staff = pd.concat(df_staff_list, ignore_index=True)

        df_department_list = []
        for key in department_csv_files:
            department_obj = s3.get_object(Bucket=ingestion_bucket, Key=key)
            department_data = department_obj["Body"].read().decode("utf-8")
            df_department_list.append(pd.read_csv(StringIO(department_data)))
        df_department = pd.concat(df_department_list, ignore_index=True)
        """
        used .merge() to left join the two dataframes
        """

        staff_department = df_staff.merge(df_department, how="left", left_on='department_id', right_on='department_id')
        star_schema_df = staff_department[[
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address"
        ]].copy()

        return star_schema_df


    except Exception as e:
        logging.error(e)
        return {"result": "Failure"}
print(dim_new_staff(s3))

