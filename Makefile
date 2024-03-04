dev:
	flask run --debug

format:
	black palbum
	isort palbum

lint:
	flake8 palbum

pr: format lint