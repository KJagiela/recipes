lint:
	flake8 .
	mypy .

lint_django:
	python manage.py makemigrations --dry-run --check
	python manage.py check --fail-level=WARNING

unit:
	pytest --dead-fixtures --dup-fixtures
	pytest \
		--cov=. \
		--junitxml=.tests_reports/junit.xml

lint_package:
	poetry check
	pip check
	safety check --bare --full-report

test: lint lint_django unit lint_package
