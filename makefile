PORT = 8080

dev-run:
	uv run uvicorn main:app --host localhost --port $(PORT) --reload

.PHONY: dev-run