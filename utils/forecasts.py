import json
import os

BOOLEAN_COMBOS = [
    [1, 1],
    [-1, 1],
    [1, -1],
    [-1, -1],
]


def build_context(
    question: dict, resolution_date: str = None, due_date: str = None
) -> str:
    """
    Build the context for a question.
    """
    context = f"""
Question: {question["question"]}

Resolution criteria: {question["resolution_criteria"]}

Background: {question["background"]}
    """

    if resolution_date:
        context = context.replace("{resolution_date}", resolution_date)

    if due_date:
        context = context.replace("{forecast_due_date}", due_date)

    return context


def update_file(file_prefix: str, forecasts: list[dict]):
    """
    Update the forecast file.
    """
    forecast_file = f"{file_prefix}.json"

    # Move current forecasts to a backup file
    backup_file = f"{file_prefix}_backup.json"
    if os.path.exists(backup_file):
        os.remove(backup_file)
    os.rename(forecast_file, backup_file)

    # Save the forecasts
    with open(forecast_file, "w") as f:
        json.dump(forecasts, f)


def find_all_forecasts(
    forecasts: list[dict],
    question_id: str | list[str],
    resolution_date: str = None,
    combination: list[int] = None,
) -> list[dict]:
    """
    Find all forecasts for a question.
    """
    return [
        f
        for f in forecasts
        if f["id"] == question_id
        and f["resolution_date"] == resolution_date
        and f["direction"] == combination
    ]
