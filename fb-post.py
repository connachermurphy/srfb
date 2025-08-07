import json
import os
import sys

import dotenv
from google.cloud import storage

dotenv.load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
FORECAST_DIR = "forecasts"

command_line_args_expected = [
    "file_prefix",
    "question_set",
    "organization",
    "N",
    "upload_to_gcs",
]
command_line_args_provided = sys.argv[1:]

if len(command_line_args_provided) != len(command_line_args_expected):
    print(f"Usage: {sys.argv[0]} {command_line_args_expected}")
    sys.exit(1)

command_line_args = dict(zip(command_line_args_expected, command_line_args_provided))

forecast_due_date = command_line_args["question_set"].replace("-llm", "")

# Load the submission file
with open(
    f"{FORECAST_DIR}/submission_{command_line_args['file_prefix']}_{command_line_args['question_set']}.json",
    "r",
) as f:
    submission = json.load(f)

# Post to GCS bucket
bucket_name = f"forecastbench-submissions/{forecast_due_date}/{GCS_BUCKET_NAME}"
bucket_path = f"{forecast_due_date}.{command_line_args['organization']}.{command_line_args['N']}.json"

command_line_args["upload_to_gcs"] = (
    command_line_args["upload_to_gcs"].lower() == "true"
)

if command_line_args["upload_to_gcs"]:
    print(f"Uploading to {bucket_name}/{bucket_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(bucket_path)
    blob.upload_from_string(json.dumps(submission))
else:
    print(f"Saving to {FORECAST_DIR}/{bucket_path}")
    with open(
        f"{FORECAST_DIR}/{forecast_due_date}.{command_line_args['organization']}.{command_line_args['N']}.json",
        "w",
    ) as f:
        json.dump(submission, f)
