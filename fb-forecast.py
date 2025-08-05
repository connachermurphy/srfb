import json
import os
import sys

import dotenv
from stochastic_radiant.forecaster import Forecaster
from tqdm import tqdm

from utils.forecasts import build_context, find_all_forecasts, update_file
from utils.questions import get_latest_question_set, get_question_count

dotenv.load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"  # using a lighter model for testing
# ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
FORECAST_DIR = "forecasts"
BOOLEAN_COMBOS = [
    [1, 1],
    [-1, 1],
    [1, -1],
    [-1, -1],
]

command_line_args_expected = [
    "file_prefix",
]
command_line_args_provided = sys.argv[1:]

if len(command_line_args_provided) != len(command_line_args_expected):
    print(f"Usage: {sys.argv[0]} {command_line_args_expected}")
    sys.exit(1)

command_line_args = dict(zip(command_line_args_expected, command_line_args_provided))

# Initialize the forecaster
forecaster = Forecaster(model=ANTHROPIC_MODEL, api_key=ANTHROPIC_API_KEY)

# Query GitHub for the latest question set object
latest_question_set = get_latest_question_set()

# Extract metadata
due_date = latest_question_set["forecast_due_date"]
question_set_name = latest_question_set["question_set"]
question_set_name_no_json = question_set_name.replace(".json", "")

print(f"Forecast due date: {due_date} ({question_set_name_no_json})")

# Create the forecast directory if it doesn't exist
os.makedirs(FORECAST_DIR, exist_ok=True)

# Create the forecast file prefix
file_prefix = f"{FORECAST_DIR}/forecasts_{command_line_args['file_prefix']}_{question_set_name_no_json}"

# Read the forecast file if it exists
forecast_file = f"{file_prefix}.json"
if os.path.exists(forecast_file):
    with open(forecast_file, "r") as f:
        forecasts = json.load(f)
else:
    forecasts = []
    with open(forecast_file, "w") as f:
        json.dump(forecasts, f)

# Number of forecasts before running
num_forecasts = len(forecasts)
print(f"Number of forecasts before running: {num_forecasts}")

# Extract the question set
questions = latest_question_set["questions"]
num_questions = len(questions)

# Save interval
save_interval = 25

for i in tqdm(range(num_questions)):
    if i % save_interval == 0:
        update_file(file_prefix, forecasts)

    question = questions[i]
    question_id = question["id"]
    num_resolution_dates, num_combinations = get_question_count(question)

    if num_resolution_dates == 1:
        resolution_dates = [None]
    else:
        resolution_dates = question["resolution_dates"]

    # Loop over the resolution dates
    for resolution_date in resolution_dates:
        if num_combinations == 1:
            combination = None

            # Check if forecast exists
            all_forecasts = find_all_forecasts(
                forecasts, question_id, resolution_date, combination
            )
            forecast_exists = len(all_forecasts)

            if forecast_exists == 0:
                context = build_context(question, resolution_date, due_date)

                try:
                    forecast, rationale = forecaster.forecast(context)

                    forecasts.append(
                        {
                            "id": question_id,
                            "source": question["source"],
                            "forecast": forecast,
                            "resolution_date": resolution_date,
                            "reasoning": rationale,
                            "direction": combination,
                        }
                    )

                except Exception:
                    print(
                        "Error forecasting question, skipping and saving current output"
                    )
                    update_file(file_prefix, forecasts)
                    continue

            elif forecast_exists == 1:
                pass
            else:
                raise ValueError(
                    f"Multiple forecasts exist for {question_id} on {resolution_date} with combination {combination}"
                )
        else:
            combinations = BOOLEAN_COMBOS

            # Loop over the combinations
            for combination in combinations:
                # Check if forecast exists
                all_forecasts = find_all_forecasts(
                    forecasts, question_id, resolution_date, combination
                )
                forecast_exists = len(all_forecasts)

                if forecast_exists == 0:
                    question_id_1 = question["id"][0]
                    question_id_2 = question["id"][1]

                    # Extract forecasts for each question
                    forecast_1 = find_all_forecasts(
                        forecasts, question_id_1, resolution_date, None
                    )
                    forecast_2 = find_all_forecasts(
                        forecasts, question_id_2, resolution_date, None
                    )

                    if len(forecast_1) == 1 and len(forecast_2) == 1:
                        forecast_1 = forecast_1[0]["forecast"]
                        forecast_2 = forecast_2[0]["forecast"]

                        forecast_1_product = (
                            forecast_1 if combination[0] == 1 else 1 - forecast_1
                        )
                        forecast_2_product = (
                            forecast_2 if combination[1] == 1 else 1 - forecast_2
                        )

                        forecast = forecast_1_product * forecast_2_product

                        forecasts.append(
                            {
                                "id": question_id,
                                "source": question["source"],
                                "forecast": forecast,
                                "resolution_date": resolution_date,
                                "reasoning": "Product of constituent forecasts (assumed to be independent).",
                                "direction": combination,
                            }
                        )
                    elif len(forecast_1) == 0 or len(forecast_2) == 0:
                        print(
                            f"Missing constituent forecasts for {question_id} on {resolution_date}, skipping."
                        )
                    else:
                        raise ValueError(
                            f"Multiple forecasts exist for {question_id} on {resolution_date}"
                        )

                elif forecast_exists == 1:
                    pass
                else:
                    raise ValueError(
                        f"Multiple forecasts exist for {question_id} on {resolution_date} with combination {combination}"
                    )
