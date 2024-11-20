from datetime import datetime
# from pprint import pprint
import pandas as pd
import boto3


#   date_id date
#   year int 
#   month int 
#   day int 
#   day_of_week int 
#   day_name varchar 
#   month_name varchar 
#   quarter 

start = '2022-01-01'
end = '2025-12-31'

def dim_date_table(start, end):

    days_names = {
    i: name for i, name in enumerate(['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday',
                    'Sunday'])
    }

    month_names = {
    i: name for i, name in enumerate([ 'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'], start=1)
    }


    df = pd.DataFrame({"Date": pd.date_range(start, end)})

    df["year"] = df.Date.dt.year
    df["month"] = df.Date.dt.month
    df["day"] = df.Date.dt.day
    df["day_of_week"] = df.Date.dt.weekday
    df["day_name"] = df.Date.dt.day_of_week.map(days_names.get)
    df["month_name"] = df.Date.dt.month.map(month_names.get)
    df["quarter"] = df.Date.dt.quarter
    df["year_half"] = (df.quarter + 1) // 2
    return print(df.tail())

dim_date_table(start, end)