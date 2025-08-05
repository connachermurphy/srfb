.PHONY: fb-forecast

fb-forecast:
	@if [ -z "$(organization)" ]; then \
		echo "Organization is required"; \
		exit 1; \
	fi
	uv run fb.py "$(organization)"