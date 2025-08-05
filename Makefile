.PHONY: fb-forecast

fb-forecast:
	@if [ -z "$(file_prefix)" ]; then \
		echo "File prefix is required"; \
		exit 1; \
	fi
	uv run fb-forecast.py "$(file_prefix)"