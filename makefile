#Check whole project with - make lint
#Formate whole project with - make format
lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy .

format:
	black .
	isort .