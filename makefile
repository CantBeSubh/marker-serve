include .env
export

PORT ?= 6969

dev-run:
	uv run uvicorn main:app --host localhost --port $(PORT) --reload

run:
	uv run uvicorn main:app --host "0.0.0.0" --port $(PORT) --reload

tmux:
	tmux new-session -A -s marker-serve

tmux-kill:
	tmux kill-session

.PHONY: dev-run run tmux tmux-kill