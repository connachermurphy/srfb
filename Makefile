.PHONY: fb-forecast, fb-prepare

fb-forecast:
	@if [ -z "$(file_prefix)" ]; then \
		echo "File prefix is required"; \
		exit 1; \
	fi
	uv run fb-forecast.py "$(file_prefix)"

fb-prepare:
	@if [ -z "$(file_prefix)" ]; then \
		echo "File prefix is required"; \
		exit 1; \
	fi
	@if [ -z "$(question_set)" ]; then \
		echo "Question set is required"; \
		exit 1; \
	fi
	@if [ -z "$(organization)" ]; then \
		echo "Organization is required"; \
		exit 1; \
	fi
	@if [ -z "$(model)" ]; then \
		echo "Model is required"; \
		exit 1; \
	fi
	@if [ -z "$(model_organization)" ]; then \
		echo "Model organization is required"; \
		exit 1; \
	fi
	uv run fb-prepare.py "$(file_prefix)" "$(question_set)" "$(organization)" "$(model)" "$(model_organization)"