VENV_DIR := ./venv
ARTIFACTS_DIR := ./python

.PHONY: create-venv
create-venv:
	python3.9 -m venv $(VENV_DIR)
	source $(VENV_DIR)/bin/activate; pip install --upgrade pip

.PHONY: install
install:
	source $(VENV_DIR)/bin/activate; pip install -r requirements.txt

.PHONY: create-python-dir
create-python-dir:
	mkdir -p $(ARTIFACTS_DIR)


.PHONY: move-files
move-files:
	source $(VENV_DIR)/bin/activate; \
	mkdir -p $(ARTIFACTS_DIR)/lib; \
	cp -r $(VENV_DIR)/lib/python3.9/site-packages/* $(ARTIFACTS_DIR)/lib/; \
	cp common_utils.py $(ARTIFACTS_DIR)


.PHONY: remove-venv
remove-venv:
	rm -rf $(VENV_DIR)

.PHONY: build-SharedLayer
build-SharedLayer: create-venv install create-python-dir move-files remove-venv