install:
	poetry install

build:
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

test-vv:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov-report term-missing --cov=page_loader

test-cov:
	poetry run pytest --cov=page_loader --cov-report xml

test-1:
	poetry run page-loader -o page_loader\tests\fixtures\ https://ru.hexlet.io/courses

test-2:
	poetry run page_loader -o page_loader\tests\fixtures\ https://skillbox.ru/

test-3:
	poetry run page_loader -o page_loader\tests\fixtures\ https://designdepot.ru/projects/

add:
	git add .

commit:
	git commit -am "Fixes"

p:
	git push