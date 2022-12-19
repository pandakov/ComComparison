VENV := .venv

ifeq ($(OS),Windows_NT)
   BIN=$(VENV)/Scripts
else
   BIN=$(VENV)/bin
endif

export PATH := $(BIN):$(PATH)

PROJECT := ComComparison

# Prepare

.venv:
	poetry install --no-root
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	poetry check

setup: .venv


# Clean

clean:
	rm -rf $(VENV)
	rm -rf data/result.h5
	rm -rf data/word2vec.model
	rm -rf data/embeddings.h5
	rm -rf data/logit.joblib


# Train

train:
	python train.py

# Run

run:
	python ranking.py

# All

all: setup run

.DEFAULT_GOAL = all
