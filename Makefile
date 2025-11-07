VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest
PLAYWRIGHT=$(VENV)/bin/playwright

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install
	
test_web_API2.0_headed:
	$(PYTEST) tests/web --headed --slowmo 200 --api-version=2.0 -v --html=report/report_api2.html --self-contained-html --log-file=report/test_run_api2.log
test_web_API2.0:
	$(PYTEST) tests/web --api-version=2.0 -v --html=report/report_api2.html --self-contained-html --log-file=report/test_run_api2.log
test_web_API1.0_headed:
	$(PYTEST) tests/web --headed --slowmo 200 --api-version=1.0 -v --html=report/report_api1.html --self-contained-html --log-file=report/test_run_api1.log
test_web_API1.0:
	$(PYTEST) tests/web --api-version=1.0 -v --html=report/report_api1.html --self-contained-html --log-file=report/test_run_api1.log