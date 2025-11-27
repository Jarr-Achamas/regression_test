# Chatbot Test Automation Suite
This README was generated on Monday, September 8, 2025.

This project contains an automated regression test suite for the chatbot web application. It is built using Python, Playwright, and the Pytest framework to ensure the application's core features are working correctly across different versions of the bot API.

## ✨ Features
- End-to-End Regression Testing: Covers the full user workflow from login to chat creation.
- Page Object Model (POM): Test logic is separated from UI interaction for better maintainability.
- Multi-Version Support: Can run tests against both API 1.0 and API 2.0 of the application.
- Sequential Test Execution: Uses pytest-dependency to ensure tests run in a strict, logical order.
- Detailed Reporting: Generates both a comprehensive HTML report (with screenshots on failure) and a detailed text log file for debugging.
- Simplified Commands: Uses a Makefile to simplify setup and test execution.
- Configuration Management: Uses a .env file for managing sensitive data like credentials.

## Prerequisites
- Python 3.9+
- pip (Python package installer)
- Git
- make (available on macOS and Linux, may need to be installed on Windows)

## ⚙️ Setup and Installation
This project uses a Makefile to automate the entire setup process.
1. Clone the repository:
```
git clone <your-repository-url>
cd CHATBOT-TESTS
```

2. Run the setup command:
This single command will create a virtual environment, install all required packages from requirements.txt, and download the necessary Playwright browser binaries.
```
make setup
```

## 📝 Configuration
Sensitive information like login credentials and URLs are managed via an environment file.
1. Create a .env file in the project root. You can copy the example.env file if one exists, or create it from scratch.
2. Edit the .env file with your specific test environment credentials:
```
ADMIN_EMAIL="your_test_email@example.com"
ADMIN_PASSWORD="your_secret_password"
```

## ▶️ Running the Tests
You can easily run the test suite for a specific API version using the provided make commands. All reports will be generated inside the report/ directory with version-specific filenames.

### 1. Active Python venv
```
source .venv/bin/activate
```

### 2. Run tests 
- For API 2.0 (open browser)
```
make test_web_API2.0_headed
```
- For API 1.0 (open browser)
```
make test_web_API1.0_headed
```
- For API 2.0
```
make test_web_API2.0
```
- For API 1.0
```
make test_web_API1.0
```

### 3. Selective Testing (Filtering) 
- You can filter tests using the MARKER, SKIP, and PATTERN variables with any of the make commands above.

| Marker | Description |
| :--- | :--- |
| `chatflow` | Chatflow creation and editing flow tests |
| `textitem` | Text item related functionality tests |
| `coupon` | Coupon functionality tests |
| `carousel` | Carousel flow tests |
| `image` | Image and Video related flow tests |
| `image_carousel_map` | Image Carousels and Image Maps flow tests |
| `image_video` | Image and Video flow tests |
| `condition_item` | Condition item related tests |
| `keyword` | Keyword, Mute, and Unmute related tests |
| `setup` | Setup/Teardown tests (Runs automatically by default) |

- Usage Examples 
  - Run only specific tests:
  ```
  make test_web_API2.0_headed MARKER=chatflow

  make test_web_API2.0_headed MARKER="coupon or carousel"
  ```
  - Skip specific tests:
  ```
  make test_web_API2.0_headed MARKER="NOT coupon"

  make test_web_API2.0_headed MARKER="NOT coupon and NOT carousel"

  make test_web_API2.0_headed SKIP=image  
  ```
  - Run and Skip only specific tests:
  ```
  make test_web_API2.0_headed MARKER="chatflow and NOT carousel"
  ```

## 📊 Viewing Reports
After a test run is complete, you can find the version-specific results in the report/ folder:
- report/report_api2.html: The HTML report for the API 2.0 test run.
- report/test_run_api2.log: The detailed text log for the API 2.0 test run.
- report/report_api1.html: The HTML report for the API 1.0 test run.
- report/test_run_api1.log: The detailed text log for the API 1.0 test run.

## 📂 Project Structure
```
CHATBOT-TESTS/
├── .venv/                  # Python virtual environment
├── report/                 # Generated test reports and logs
├── tests/
│   ├── web/                # Contains web application tests
│   │   ├── page_objects/   # Page Object Model classes for different UI components
│   │   │   ├── __init__.py
│   │   │   ├── bot_list_view_page.py
│   │   │   ├──login_page.py
│   │   │   └── ...
│   │   ├── test_admin_bot.py # The main test script with test cases
│   │   └── test_data.py      # Test data used by the test scripts
│   └── mobile/             # Placeholder for future mobile tests
│
├── .env                    # Local environment variables (DO NOT COMMIT)
├── conftest.py             # Pytest fixtures and hooks (setup, teardown, failure handling)
├── init_chatbot_tests.py   # Initial setup or utility script
├── Makefile                # Command shortcuts for setup and testing
├── pytest.ini              # Pytest configuration and marker definitions
├── README.md               # This file
├── requirements.txt        # List of Python dependencies
└── web_config.py           # Main configuration file (URLs, constants)
```

## 🛠️ Key Technologies
- Python 3.9+
- Playwright: For browser automation.
- Pytest: As the test runner framework.
- pytest-html: For generating HTML reports.
- pytest-dependency: For controlling test execution order.
- GNU Make: For command automation.