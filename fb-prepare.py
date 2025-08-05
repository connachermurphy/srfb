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

# Create submission dictionary
submission = {
    "organization": command_line_args["organization"],
    "model": command_line_args["model"],
    "model_organization": command_line_args["model_organization"],
    "question_set": command_line_args["question_set"],
    "forecasts": forecasts,
}

# Save the submission file
with open(
    f"{FORECAST_DIR}/submission_{command_line_args['file_prefix']}_{command_line_args['question_set']}.json",
    "w",
) as f:
    json.dump(submission, f)
