import pytest
import logging
from playwright.sync_api import Page
from pathlib import Path
from tests.web.test_data import IMAGES

# --- Import config and page objects ---
from config import ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_URL, BOT_NAMES
from tests.web.page_objects import LoginPage, BotListViewPage

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)
logger = logging.getLogger(__name__)

# --- Command-line Option for API Version ---
def pytest_addoption(parser):
    """Adds a custom command-line option to pytest for API version."""
    parser.addoption(
        "--api-version", action="store", default="2.0", help="Specify the API version to test: 1.0 or 2.0"
    )

# --- Test Collection Hook: Ensure setup tests run first ---
def pytest_collection_modifyitems(config, items):
    """Reorder tests so setup-marked tests run before all others."""
    setup_tests = []
    other_tests = []
    
    for item in items:
        if item.get_closest_marker("setup"):
            setup_tests.append(item)
        else:
            other_tests.append(item)
    
    items[:] = setup_tests + other_tests

# --- Session-Scoped Fixtures ---
# These are set up once for the entire test run for efficiency.
@pytest.fixture(scope="session")
def api_version(request) -> str:
    """Gets the API version from the command line, available for the whole session."""
    return request.config.getoption("--api-version")

@pytest.fixture(scope="session")
def bot_name(api_version: str) -> str:
    """Provides the correct bot name STRING based on the session's API version."""
    return BOT_NAMES[api_version]["name"]

# --- Core Setup Fixture ---
@pytest.fixture(scope="function")
def logged_in_chatflow_page(page: Page, bot_name: str) -> Page:
    """
    Provides a page object that is already logged in and has navigated to the correct bot's chatflow.
    
    The `scope="function"` ensures this runs fresh for every single test, guaranteeing isolation.
    """
    logger.info("--- Fixture Setup: Starting new test in a clean browser state ---")

    # Step 1: Login
    # The 'page' fixture is provided automatically by pytest-playwright.
    # Your LoginPage object should handle navigating to the URL.
    login_page = LoginPage(page)
    login_page.navigate(ADMIN_URL)
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    logger.info(f"Fixture: Login successful as {ADMIN_EMAIL}.")

    # Step 2: Search for and open the specified bot
    bot_list_view_page = BotListViewPage(page)
    bot_list_view_page.search_and_select_bot(bot_name)
    logger.info(f"Fixture: Navigation to bot '{bot_name}' complete. Page is ready for the test.")

    # The fixture hands over control to the test function
    yield page

    # Teardown: This code runs after the test finishes.
    # The pytest-playwright `page` fixture handles closing the page/context automatically.
    logger.info("--- Fixture Teardown: Test finished ---")


# --- Set project root ---
@pytest.fixture(scope="session")
def project_root() -> Path:
    """A fixture that returns the root directory of the project."""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def image_path_factory(project_root: Path):
    """
    A factory fixture that returns a function to get the full path of any test image.
    """
    def get_image_path(image_name: str) -> str:
        """
        Retrieves the full path for an image using its logical name.
        """
        if image_name not in IMAGES:
            raise FileNotFoundError(f"Image '{image_name}' is not defined in test_data/assets.py.")
        
        file_name = IMAGES[image_name]
        path = project_root / "uploaddata" / file_name
        
        if not path.is_file():
            raise FileNotFoundError(f"Image file not found at path: {path}")
            
        return str(path)
        
    return get_image_path