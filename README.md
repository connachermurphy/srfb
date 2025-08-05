# srfb: Stochastic Radiant ForecastBench Submission

## References
The ForecastBench Wiki is available [here](https://github.com/forecastingresearch/forecastbench/wiki/How-to-submit-to-ForecastBench).

## Grab the question set
`get_latest_question_set()` from `utils.questions`.

## Question types
1. Standard
1. Combination
1. Multiple resolution dates

Anything else?


Target
```json
{
    "id": {
        "description": "A unique identifier string given `source`, corresponding to the `id` from the question in the question set that's being forecast. e.g. 'd331f271'. Required.",
        "type": "string | array<string>"
    },
    "source": {
        "description": "Where the data comes from, corresponding to the `source` from the question in the question set that's being forecast. e.g. 'metaculus'. Required.",
        "type": "string"
    },
    "forecast": {
        "description": "The forecast. A float in [0,1]. e.g. 0.5. Required.",
        "type": "number"
    },
    "resolution_date": {
        "description": "The resolution date this forecast corresponds to. e.g. '2025-01-01'. `null` for market questions. Required.",
        "type": "string | null"
    },
    "reasoning": {
        "description": "The rationale underlying the forecast. e.g. ''. Optional.",
        "type": "string | null"
    },
    "direction": {
        "description": "If `id` is a string, the value here should be `null`. If `id` has an array value, then this is a forecast on a combination question and the value here should be an array of the same length as `id`. Each entry is an integer in {-1, 1}. If the value is 1, it means the forecast is in the normal direction of the question. If the value is -1, it means the forecast is for the negated question. e.g. if `id` is an array of length 2, where Q1 corresponds to the first entry of the array in `id` and Q2 corresponds to the second entry, to provide the forecast for P(¬Q1 AND Q2), the value for `direction` would be [-1, 1]. All possible values are: [1,1], [-1,1], [1,-1], [-1,-1], corresponding to the 4 Boolean combinations of the two questions in the `id` array. e.g. [1,1]. Default: null. Required.",
        "type": "array<number> | null"
    }
}
```


Example usage:
make fb-forecast organization="Stochastic Radiant"