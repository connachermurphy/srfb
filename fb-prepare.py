import json
import sys

FORECAST_DIR = "forecasts"

command_line_args_expected = [
    "file_prefix",
    "question_set",
    "organization",
    "model",
    "model_organization",
]
command_line_args_provided = sys.argv[1:]

if len(command_line_args_provided) != len(command_line_args_expected):
    print(f"Usage: {sys.argv[0]} {command_line_args_expected}")
    sys.exit(1)

command_line_args = dict(zip(command_line_args_expected, command_line_args_provided))

# Load the forecast file
forecast_file = f"{FORECAST_DIR}/forecasts_{command_line_args['file_prefix']}_{command_line_args['question_set']}.json"
with open(forecast_file, "r") as f:
    forecasts = json.load(f)

# TODO: Create the submission file

# TODO: save the submission file
