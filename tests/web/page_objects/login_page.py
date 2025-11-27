# page_objects/login_page.py
from playwright.sync_api import Page, expect
from config import WAITING_TIMEOUT_MS

class LoginPage:
    """Page object for the login screen."""
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='pass']")
        self.login_button = page.locator("button.show-mail-login")
        self.new_app_button = page.locator("button[hint='新しいアプリ作成']")
    # ==================================================================
    

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Open anybot site ---
    def navigate(self, url: str):
        """Navigates to the login page."""
        self.page.goto(url)

    # --- Login to anybot ---
    def login(self, email: str, password: str):
        """Fills login credentials and logs in."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        # Wait for a reliable element on the next page to confirm login
        expect(self.new_app_button).to_be_visible(timeout=WAITING_TIMEOUT_MS)