# page_objects/chatflow_page.py
from playwright.sync_api import Page, expect
from config import WAITING_TIMEOUT_MS

class ChatflowPage:
    """Page object for the Chatflow (会話フロー) screen."""
    def __init__(self, page: Page):
        self.page = page
        # Locators for different panes
        self.group_pane = page.locator("section[class='left-pane group-pane']")
        self.action_pane = page.locator("section[class='left-pane action-pane']")
        self.canv_pane = page.locator("section[class='center-pane canv']")
    # ==================================================================
    

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Test verify UI in 会話フロー page ---
    def verify_ui_elements_are_visible(self):
        """Checks that all key UI panes and their elements are visible."""
        # Verify Group Pane
        expect(self.group_pane).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.group_pane.get_by_text("グループ一覧", exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.group_pane.get_by_role("button", name="グループ追加")).to_be_visible(timeout=WAITING_TIMEOUT_MS)

        # Verify Action Pane
        expect(self.action_pane).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.action_pane.get_by_text("会話・アクション一覧", exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.action_pane.get_by_role("button", name="会話を追加")).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        
        # Verify Canvas Pane (Initial Greeting)
        expect(self.canv_pane).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.canv_pane.locator("input[data-value='最初の挨拶']")).to_be_visible(timeout=WAITING_TIMEOUT_MS)