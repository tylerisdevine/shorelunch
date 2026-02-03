.PHONY: help lint format check-format check-lint test-lint

help:
	@echo "Available commands:"
	@echo "  make lint         - Run black and ruff checks"
	@echo "  make format       - Auto-format code with black and ruff"
	@echo "  make check-format - Check code formatting without making changes"
	@echo "  make check-lint   - Check for linting issues without fixing"

# Run both black and ruff checks
lint: check-format check-lint

# Check formatting without making changes
check-format:
	@echo "Checking code formatting with black..."
	docker run --rm -v "$$(pwd):/app" shorelunch:latest black --check .

# Check for linting issues without fixing
check-lint:
	@echo "Checking for linting issues with ruff..."
	docker run --rm -v "$$(pwd):/app" shorelunch:latest ruff check .

# Auto-format code with black and ruff
format:
	@echo "Formatting code with black..."
	docker run --rm -v "$$(pwd):/app" shorelunch:latest black .
	@echo "Fixing auto-fixable issues with ruff..."
	docker run --rm -v "$$(pwd):/app" shorelunch:latest ruff check --fix .
	@echo "Done! Code has been formatted."
