dev:
	flask run --debug

format:
	black .
	isort *.py