SHELL = /bin/bash

# Environment
.PHONY: setup
setup:
	python3 -m venv ~/.data2bot && \
	source ~/.data2bot/bin/activate && \
	pip3 install -r configs/requirements.txt && \
	cp configs/config.ini.example config.ini

# Cleaning
.PHONY: clean
clean: 
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage
	black .

.PHONY: run
run: 
	python3 scripts/start.py

.PHONY: serve
serve: 
	streamlit run scripts/streamlit_app.py

.PHONY: help
help:
	@echo "Commands:"
	@echo "setup    : creates a virtual environment (data2bot) for the project."
	@echo "clean   : deletes all unnecessary files and executes style formatting."
	@echo "run   	: starts running the pipeline."
	@echo "serve	: starts the streamlit local host server for visualization"