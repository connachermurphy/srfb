from stochastic_radiant.forecaster import Forecaster

from utils.questions import get_question_count

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


def get_question_forecasts(
    question: dict,
    forecasts: list[dict],
    forecaster: Forecaster,
    due_date: str = None,
) -> list[dict]:
    """
    Get the forecasts for a question.
    """
    question_forecasts = []
    question_forecasts_missing = []

    num_resolution_dates, num_combinations = get_question_count(question)

    if num_resolution_dates == 1:  # Single resolution date
        if num_combinations == 1:  # Single resolution date, single combination
            context = build_context(question, due_date=due_date)

            forecast, rationale = forecaster.forecast(context)

            question_forecasts.append(
                {
                    "id": question["id"],
                    "source": question["source"],
                    "forecast": forecast,
                    "resolution_date": None,
                    "reasoning": rationale,
                    "direction": None,
                }
            )
        else:  # Single resolution date, multiple combinations
            # Grab consistuent questions
            question_id_1 = question["id"][0]
            question_id_2 = question["id"][1]

            # Extract forecasts for each question
            forecast_1 = next((f for f in forecasts if f["id"] == question_id_1), None)
            forecast_2 = next((f for f in forecasts if f["id"] == question_id_2), None)

            forecast_1 = forecast_1["forecast"] if forecast_1 else None
            forecast_2 = forecast_2["forecast"] if forecast_2 else None

            if forecast_1 is None or forecast_2 is None:
                # TODO: add more question details
                question_forecasts_missing.append(
                    {
                        "id": question["id"],
                        "source": question["source"],
                    }
                )
            else:
                for combo in BOOLEAN_COMBOS:
                    forecast_1_product = forecast_1 if combo[0] == 1 else 1 - forecast_1
                    forecast_2_product = forecast_2 if combo[1] == 1 else 1 - forecast_2

                    forecast = forecast_1_product * forecast_2_product

                    question_forecasts.append(
                        {
                            "id": question["id"],
                            "source": question["source"],
                            "forecast": forecast,
                            "resolution_date": None,
                            "reasoning": "Calculated programmatically from constituent forecasts under the assumption that the constituent questions are independent.",
                            "direction": combo,
                        }
                    )

    else:  # Multiple resolution dates
        for resolution_date in question["resolution_dates"]:
            if num_combinations == 1:  # Multiple resolution dates, single combination
                context = build_context(
                    question, resolution_date=resolution_date, due_date=due_date
                )

                forecast, rationale = forecaster.forecast(context)

                question_forecasts.append(
                    {
                        "id": question["id"],
                        "source": question["source"],
                        "forecast": forecast,
                        "resolution_date": resolution_date,
                        "reasoning": rationale,
                        "direction": None,
                    }
                )
            else:  # Multiple resolution dates, multiple combinations
                # Grab consistuent questions
                question_id_1 = question["id"][0]
                question_id_2 = question["id"][1]

                # Extract forecasts for each question
                forecast_1 = next(
                    (
                        f
                        for f in forecasts
                        if f["id"] == question_id_1
                        and f["resolution_date"] == resolution_date
                    ),
                    None,
                )
                forecast_2 = next(
                    (
                        f
                        for f in forecasts
                        if f["id"] == question_id_2
                        and f["resolution_date"] == resolution_date
                    ),
                    None,
                )

                forecast_1 = forecast_1["forecast"] if forecast_1 else None
                forecast_2 = forecast_2["forecast"] if forecast_2 else None

                if forecast_1 is None or forecast_2 is None:
                    question_forecasts_missing.append(
                        {
                            "id": question["id"],
                            "source": question["source"],
                        }
                    )
                else:
                    for combo in BOOLEAN_COMBOS:
                        forecast_1_product = (
                            forecast_1 if combo[0] == 1 else 1 - forecast_1
                        )
                        forecast_2_product = (
                            forecast_2 if combo[1] == 1 else 1 - forecast_2
                        )

                        forecast = forecast_1_product * forecast_2_product

                        forecasts.append(
                            {
                                "id": question["id"],
                                "source": question["source"],
                                "forecast": forecast,
                                "resolution_date": None,
                                "reasoning": "Calculated programmatically from constituent forecasts under the assumption that the constituent questions are independent.",
                                "direction": combo,
                            }
                        )

    return question_forecasts, question_forecasts_missing
