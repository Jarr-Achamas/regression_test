from playwright.sync_api import Page, Locator, expect
from playwright.sync_api._generated import Response
from config import WAITING_TIMEOUT_MS

def deploy_and_wait_for_response(page: Page, deploy_button: Locator, deploy_popup: Locator, ok_button: Locator, deploy_complete_popup: Locator, url_glob: str):
    """
    Clicks a locator and waits for a specific API response.
    
    Args:
        page: The Playwright Page object.
        deploy_button: The locator of the element to click (e.g., a deploy button).
        deploy_popup: The locator of the deploy confirmation popup.
        ok_button: The locator of the OK button in the popup.
        deploy_complete_popup: The locator of the deploy completion popup.
        url_glob: A glob pattern for the API URL to wait for (e.g., "**/app.json").

    Raises:
        AssertionError: If the API response is not successful (status not 2xx).
        TimeoutError: If the API response is not received within the timeout.
    """
    try:
        deploy_button.click()
        expect(deploy_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        
        with page.expect_response(url_glob, timeout=WAITING_TIMEOUT_MS * 2) as response_info:
            ok_button.click()
        
        response = response_info.value
        if not response.ok:
            raise AssertionError(f"Image upload API failed with status {response.status}: {response.text()}")
        
        # Assert that the API call was successful
        assert response.ok, f"API call to {url_glob} failed with status: {response.status}"
        expect(deploy_complete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    except TimeoutError:
        print(f"Error: Timed out waiting for {url_glob} API response.")
        raise
