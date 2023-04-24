VENV := .venv

ifeq ($(OS),Windows_NT)
   BIN=$(VENV)/Scripts
else
   BIN=$(VENV)/bin
endif

export PATH := $(BIN):$(PATH)

.venv:
	poetry install --no-root
	poetry check

setup: .venv

activate: setup
	poetry shell