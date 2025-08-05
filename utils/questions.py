import requests

# Constants
URL = "https://raw.githubusercontent.com/forecastingresearch/forecastbench-datasets/main/datasets/question_sets"


def get_question_set(question_set_name: str) -> dict:
    """
    Get a question set from the dataset.
    """
    url = f"{URL}/{question_set_name}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_latest_question_set_name() -> str:
    """
    Get the name of the latest question set from the latest-llm.json file.
    """
    url = f"{URL}/latest-llm.json"

    response = requests.get(url)
    response.raise_for_status()

    return response.text


def get_latest_question_set():
    """
    Get the latest question set, using the pointer from the latest-llm.json file.
    """
    # Get the name of the latest question set
    latest_question_set_name = get_latest_question_set_name()

    # Get the question set from the dataset
    latest_question_set = get_question_set(latest_question_set_name)

    return latest_question_set


def _validate_combination_count(num_combinations: int) -> None:
    """
    Validate the combination count.
    """
    if num_combinations != 1 and num_combinations != 2:
        raise ValueError(
            f"Combination count is not valid: {num_combinations}. Must be 1 or 2."
        )


def get_question_count(question: dict) -> tuple[int, int]:
    """
    Get the type of a question.
    """
    resolution_dates = question["resolution_dates"]
    combination_of = question["combination_of"]

    if isinstance(resolution_dates, list):
        num_resolution_dates = len(resolution_dates)
    elif isinstance(resolution_dates, str):
        num_resolution_dates = 1
    else:
        raise ValueError("Resolution dates is not a list or a string")

    if isinstance(combination_of, list):
        num_combinations = len(combination_of)
    elif isinstance(combination_of, str):
        num_combinations = 1
    else:
        raise ValueError("Combination of is not a list")

    _validate_combination_count(num_combinations)

    return num_resolution_dates, num_combinations
