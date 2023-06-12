.PHONY: doc

# commands
style:
	@flake8 src
	@pydocstyle src

load: 
	@gdown --fuzzy https://drive.google.com/file/d/16bINNiCQs4P3W58Qj5FGfPf-GdfWRTC_/view?usp=sharing -O src/spellchecker/models/prefix_tree.pickle
	@gdown --fuzzy https://drive.google.com/file/d/1XLUZ1qSliuDdqiLQPumLyzZSP1n3ZWS8/view?usp=sharing -O src/spellchecker/models/language_model.pickle
	@gdown --fuzzy https://drive.google.com/file/d/1UE09HPhwmw2nkZoqTB0hIXeWYJR67sp-/view?usp=sharing -O index/buided_index.pickle

load_data:    
	@gdown --fuzzy https://drive.google.com/file/d/1ZuLSl21KmbKdzWq69GY-kMBq5qE8GADf/view?usp=sharing -O data/data.csv
    
build:
	@python3 build_index.py
	@python3 src/spellchecker/build_models.py

test:
	@pytest tests

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt
	@playwright install

local:
	@pybabel compile -D app -d src/locales/ -l ru
	@pybabel compile -D app -d src/locales/ -l en

doc: 
	@cd doc && make html

run:
	@streamlit run src/app/MainPage.py

wheel:
	@pyproject-build -w -n

clean:
	@git clean -fdx
