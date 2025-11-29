include .env
export

PORT ?= 6969

dev-run:
	uv run uvicorn main:app --host localhost --port $(PORT) --reload

run:
	uv run uvicorn main:app --host "0.0.0.0" --port $(PORT) --workers 3

hyper-dev-run:
	uv run hypercorn --access-log - --error-log - main:app --bind 0.0.0.0:$(PORT) --reload

hyper-run:
	uv run hypercorn --access-log - --error-log - main:app --bind 0.0.0.0:$(PORT) --workers 3

tmux:
	tmux new-session -A -s marker-serve

tmux-kill:
	tmux kill-session

dbuild:
	@echo "Building..."
	docker build --platform linux/amd64 -t marker-serve .

drun:
	docker run --rm -p 80:80 --platform linux/amd64 --name marker-serve marker-serve

dpush:

	@echo "Getting git commit hash..."
	$(eval COMMIT_HASH := $(shell git rev-parse --short HEAD))
	@echo "Building..."
	docker build -t holyc0w/marker-serve:${COMMIT_HASH} -t holyc0w/marker-serve:latest --platform linux/amd64  .
	@echo "Pushing..."
	docker push holyc0w/marker-serve:${COMMIT_HASH}
	docker push holyc0w/marker-serve:latest
