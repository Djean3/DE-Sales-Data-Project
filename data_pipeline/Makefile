deploy-development:
	sls deploy --stage development

create-requirements:
	poetry export -f requirements.txt --output requirements.txt --without dev

run_local:
	poetry run python run_local.py