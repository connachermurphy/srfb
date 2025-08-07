# srfb: Stochastic Radiant ForecastBench Submission
I use [Stochastic Radiant](https://github.com/connachermurphy/stochastic-radiant) to create a submission for [ForecastBench](https://www.forecastbench.org/). Both of these tools are intended for demonstration purposes. However, I plan to continue development of Stochastic Radiant, with associated evaluation in this repo.

## References
The ForecastBench Wiki is available [here](https://github.com/forecastingresearch/forecastbench/wiki/How-to-submit-to-ForecastBench).

## Usage
The forecast routine requires a `.env` file in the project root:
```
ANTHROPIC_API_KEY={your_anthropic_api_key}
```
Use `fb-forecast` to generate forecasts on the latest question set (`question_set` below). Example usage:
```bash
make fb-forecast file_prefix="srfb_demo" model="claude-3-5-haiku-20241022"
```

Arguments:
- `file_prefix` controls the output file name (forecasts_`file_prefix`_`question_set`)
- `model` specifies the model (must be an [Anthropic model](https://docs.anthropic.com/en/docs/about-claude/models/overview), as Stochastic Radiant only supports Antrhopic at present)

Use `fb-prepare` to prepare a ForecastBench submission file. Example usage:
```bash
make fb-prepare file_prefix="srfb_demo" question_set="2025-08-03-llm" organization="Stochastic Radiant" model="claude-3-5-haiku-20241022" model_organization="Anthropic"
```

Arguments:
- `file_prefix`: Identifier for the forecast files (e.g., "srfb_demo")
- `question_set`: Name of the question set being forecasted (e.g., "2025-08-03-llm") 
- `organization`: Your organization name (for the ForecastBench leaderboard)
- `model`: The model used to generate forecasts
- `model_organization`: Organization that created the model

Use `fb-post` to post a forecast set to the relevant GCS bucket. Example usage:
```bash
make fb-post file_prefix="srfb_demo" question_set="2025-08-03-llm" organization="Stochastic Radiant" N=1 upload_to_gcs=False
```
- `file_prefix`: Identifier for the forecast files (e.g., "srfb_demo")
- `question_set`: Name of the question set being forecasted (e.g., "2025-08-03-llm") 
- `organization`: Your organization name (for the ForecastBench leaderboard)
- `N`: the submission number (integer)

## Contributions
Please contact me if you're interested in contributing. These submission tools and Stochastic Radiant are both in active development.