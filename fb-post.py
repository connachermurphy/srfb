import os
import subprocess
import sys
import urllib.parse

import dotenv

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

submission_path = f"{FORECAST_DIR}/submission_{command_line_args['file_prefix']}_{command_line_args['question_set']}.json"

# Post to GCS bucket
sub_bucket_name = f"{forecast_due_date}/{GCS_BUCKET_NAME}"
filename = f"{forecast_due_date}.{command_line_args['organization']}.{command_line_args['N']}.json"
filename_full = f"{sub_bucket_name}/{filename}"
encoded_filename_full = urllib.parse.quote(filename_full, safe="/")

command_line_args["upload_to_gcs"] = (
    command_line_args["upload_to_gcs"].lower() == "true"
)

if command_line_args["upload_to_gcs"]:
    print("Uploading to GCS")

    token = subprocess.check_output(
        ["gcloud", "auth", "print-access-token"], text=True
    ).strip()
    url = f"https://storage.googleapis.com/upload/storage/v1/b/forecastbench-submissions/o?uploadType=media&name={encoded_filename_full}"

    subprocess.run(
        [
            "curl",
            "-X",
            "POST",
            "-H",
            f"Authorization: Bearer {token}",
            "-H",
            "Content-Type: application/json",
            "--data-binary",
            f"@{submission_path}",
            url,
        ],
        check=True,
    )


# Create a local copy with the appropriate name
local_submission_path = f"{FORECAST_DIR}/{filename}"

subprocess.run(
    [
        "cp",
        submission_path,
        local_submission_path,
    ],
)
