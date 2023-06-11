.PHONY: doc

# commands
lint:
	@flake8 src
	@pydocstyle src

test:
	@playwright install
	@pytest

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

localisation:
	@pybabel compile -D app -d src/locales/ -l ru
	@pybabel compile -D app -d src/locales/ -l en

doc:
	@cd doc && make html

build: install lint localisation doc

run:
	@python3 src/spellchecker/build_models.py
	@export PYTHONPATH="${PYTHONPATH}:{pwd}/src"
	@streamlit run src/app/MainPage.py

wheel:
	@pyproject-build -w -n

clean:
	@git clean -fdx
