dev:
	flask run --debug

format:
	black .
	isort *.py

lint:
	flake8 app.py

pr: format lint