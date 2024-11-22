# placeholder for Lambda2
def lambda_handler(event, context):
    """
    Event input:
    {"response": 200,
                "csv_files_written": csv_files_written (list),
                "timestamp_json_files_written": timestamp_json_files_written (list)}"""
    speech = "Hello World!"
    print(speech)
    return speech
