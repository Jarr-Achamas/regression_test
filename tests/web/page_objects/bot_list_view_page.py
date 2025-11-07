# page_objects/bot_list_view_page.py
from playwright.sync_api import Page, expect
from config import WAITING_TIMEOUT_MS

class BotListViewPage:
    """Page object for the main bot list view after login."""
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.all_apps_button = page.locator("dd[hint='全てのアプリ一覧']")
        self.search_input = page.get_by_placeholder("ボット名またはIDで検索")
        self.bot_list_view = page.locator(".list-view")
        self.conversation_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.conversation_popup.locator(".icon.close")

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Test search and select bot ---
    def search_and_select_bot(self, bot_name: str):
        """Searches for a bot by name, selects it, and handles the popup."""
        self.all_apps_button.click()
        self.search_input.fill(bot_name)
        self.search_input.press("Enter")
        expect(self.bot_list_view).to_contain_text(bot_name, timeout=WAITING_TIMEOUT_MS)
        self.bot_list_view.get_by_text(bot_name).click()
        # Close popup.
        expect(self.conversation_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.close_popup_button.click()
        expect(self.conversation_popup).to_be_hidden()