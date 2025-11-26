VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest
PLAYWRIGHT=$(VENV)/bin/playwright

# Test selection options (optional)
# MARKER: Select tests by marker (e.g., MARKER=chatflow, MARKER="chatflow and not image")
# PATTERN: Select tests by name pattern (e.g., PATTERN="test_coupon")
#   Note: When using PATTERN, setup tests are automatically included unless SKIP=setup
# SKIP: Skip tests by marker (e.g., SKIP=image)
MARKER ?=
PATTERN ?=
SKIP ?=

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install

# Build pytest selection args - always include setup unless SKIP=setup
SKIP_SETUP = $(findstring setup,$(SKIP))
INCLUDE_SETUP = $(if $(SKIP_SETUP),,setup or )
MARKER_EXPR = $(if $(MARKER),$(MARKER)$(if $(SKIP), and not $(SKIP),),$(if $(SKIP),not $(SKIP),))
PYTEST_MARKER = $(if $(MARKER_EXPR),-m "$(INCLUDE_SETUP)$(MARKER_EXPR)",)
PYTEST_PATTERN = $(if $(PATTERN),-k "$(if $(SKIP_SETUP),$(PATTERN),test_clear_previous_created_data or ($(PATTERN)))",)
PYTEST_SELECT = $(PYTEST_MARKER)$(PYTEST_PATTERN)

test_web_API2.0_headed:
	$(PYTEST) tests/web --headed --slowmo 200 --api-version=2.0 -v --html=report/report_api2.html --self-contained-html --log-file=report/test_run_api2.log $(PYTEST_SELECT)
test_web_API2.0:
	$(PYTEST) tests/web --api-version=2.0 -v --html=report/report_api2.html --self-contained-html --log-file=report/test_run_api2.log $(PYTEST_SELECT)
test_web_API1.0_headed:
	$(PYTEST) tests/web --headed --slowmo 200 --api-version=1.0 -v --html=report/report_api1.html --self-contained-html --log-file=report/test_run_api1.log $(PYTEST_SELECT)
test_web_API1.0:
	$(PYTEST) tests/web --api-version=1.0 -v --html=report/report_api1.html --self-contained-html --log-file=report/test_run_api1.log $(PYTEST_SELECT)