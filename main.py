import json
import os

import dotenv
from stochastic_radiant.forecaster import Forecaster
from tqdm import tqdm

from utils.forecasts import get_question_forecasts
from utils.questions import get_latest_question_set

dotenv.load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"  # using a lighter model for testing
# ANTHROPIC_MODEL = "claude-sonnet-4-20250514"


def main():
    # Initialize the forecaster
    forecaster = Forecaster(model=ANTHROPIC_MODEL, api_key=ANTHROPIC_API_KEY)

    # Query GitHub for the latest question set object
    latest_question_set = get_latest_question_set()

    # Extract metadata
    due_date = latest_question_set["forecast_due_date"]
    question_set_name = latest_question_set["question_set"]
    question_set_name_no_json = question_set_name.replace(".json", "")
    file_prefix = f"forecasts/forecasts_{question_set_name_no_json}"

    print(f"Forecast due date: {due_date} ({question_set_name})")

    # Extract the question set
    questions = latest_question_set["questions"]
    num_questions = len(questions)

    print(f"Number of questions: {num_questions}")

    forecasts = []
    forecasts_missing = []

    # Periodically save the forecasts
    save_interval = 100

    # for i in range(num_questions):
    for i in tqdm(range(num_questions)):
        # Extract the question object
        question = questions[i]

        # Get the question forecasts
        question_forecasts, question_forecasts_missing = get_question_forecasts(
            question, forecasts, forecaster, due_date
        )
        forecasts.extend(question_forecasts)
        forecasts_missing.extend(question_forecasts_missing)

        if i % save_interval == 0:
            with open(f"{file_prefix}_{i}.json", "w") as f:
                json.dump(forecasts, f)

    # Save the forecasts
    print(f"Saving forecasts to {file_prefix}.json")
    with open(f"{file_prefix}.json", "w") as f:
        json.dump(forecasts, f)
    print(f"Saved forecasts to {file_prefix}.json")

    print("Number of forecasts:", len(forecasts))
    print("Number of missing forecasts:", len(forecasts_missing))

    print("Creating submission dictionary...")

    # Create ForecastBench submission dictionary
    submission_dict = {
        "organization": "Stochastic Radiant",
        "model": "claude-3-5-haiku-20241022",
        "model_organization": "Anthropic",
        "question_set": question_set_name,
        "forecasts": forecasts,
    }

    # Save the submission dictionary
    with open(f"{file_prefix}_submission.json", "w") as f:
        json.dump(submission_dict, f)

    print(f"Saved submission dictionary to {file_prefix}_submission.json")


if __name__ == "__main__":
    main()
