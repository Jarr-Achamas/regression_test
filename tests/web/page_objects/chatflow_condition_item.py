# page_objects/chatflow_condition_item.py
from playwright.sync_api import Page, Locator, expect
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    GROUP_NAME_KAIWA, GROUP_NAME_CAROUSEL, CHAT_FLOW_TEXT_ITEMS, CHAT_FLOW_CAROUSEL_NAME,
    GROUP_NAME_CONDITION, CONDITION_ITEM_NAME, CONDITION_VALUE,
    )
 
class CreateConditionItem:
    """Page object for the test create Condition Item in 会話フロー screen."""
    def __init__(self, page: Page):
        self.page = page
        # Access chat flow screen
        self.header_app_tab = page.locator("//a[@name='bot_edit_view']")
        # Tutorials popup
        self.tutorials_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.tutorials_popup.locator(".icon.close")
        # Group creation
        self.add_group_button = page.get_by_role("button", name="グループ追加")
        self.add_group_newgroup = page.locator("dd[act='group']")
        self.new_name_textbox = page.locator("li.editing").get_by_role("textbox")
        self.group_list = page.locator("ul.groups")
        # For tesxtitem and carousel creation
        self.add_kaiwa_text = page.locator("dd[rt='text']")
        self.kaiwa_text_msg = page.locator("textarea.msg.with-emoticon")
        self.add_kaiwa_carousel = page.locator("dd[rt='card']")
        self.react_content_cards = page.locator("div[class='cells rt-card rt-image rt-video rt-audio rt-imagemap rt-flyer rt-imagecard rt-flex']")
        # Chatflow condition item creation
        self.add_kaiwa_button = page.get_by_role("button", name="会話を追加")
        self.add_kaiwa_condition_item = page.locator("dd[rt='logical']")
        self.kaiwa_text_list = page.locator(".actions")
        # Condition item setting
        self.moshi_dropdown = page.locator("div[class='ui-dropdown']").first
        self.moshi_dropdown_options = page.locator("ul[class='ui-dropdown-opts']")
        self.condition_input = page.locator(".condition-box input[name='condition']")
        
    # ==================================================================


    # ==================================================================
    # Reusable Helper Methods
    # ==================================================================
    # --- Reusable Helper Methods for Groups (ChatFlow) ---
    def _close_tutorials_popup_if_visible(self):
        """Helper to close the tutorials popup if it is visible."""
        expect(self.tutorials_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.close_popup_button.click()
        expect(self.tutorials_popup).to_be_hidden(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for Group1 Creation ---
    def _create_group1_if_not_exists(self):
        """Helper to create Group1 if it does not exist."""
        if not self.group_list.get_by_text(GROUP_NAME_KAIWA).is_visible():
            # Create Group1 if it does not exist
            self.add_group_button.hover()
            self.add_group_newgroup.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(GROUP_NAME_KAIWA)
            self.new_name_textbox.press("Enter")
            # Close popup.
            self._close_tutorials_popup_if_visible()
            # Create Textitem1 under Group1
            self.add_kaiwa_button.hover()
            self.add_kaiwa_text.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(CHAT_FLOW_TEXT_ITEMS[0])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(CHAT_FLOW_TEXT_ITEMS[0], timeout=WAITING_TIMEOUT_MS)
            # Add text to Textitem1
            self.kaiwa_text_msg.last.fill(CHAT_FLOW_TEXT_ITEMS[4])
            self.kaiwa_text_msg.last.press("Enter")
            # Close popup.
            self._close_tutorials_popup_if_visible()
            expect(self.kaiwa_text_msg.last).to_have_value(CHAT_FLOW_TEXT_ITEMS[4])
        expect(self.group_list.get_by_text(GROUP_NAME_KAIWA)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for Group2 Creation ---
    def _create_group2_if_not_exists(self):
        """Helper to create Group2 if it does not exist."""
        if not self.group_list.get_by_text(GROUP_NAME_CAROUSEL).is_visible():
            # Create Group2 if it does not exist
            self.add_group_button.hover()
            self.add_group_newgroup.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(GROUP_NAME_CAROUSEL)
            self.new_name_textbox.press("Enter")
            # Close popup.
            self._close_tutorials_popup_if_visible()
            # Create Carousel1 under Group2
            for i in range(2):
                # 会話追加 (カルーセル)
                self.add_kaiwa_button.hover()
                self.add_kaiwa_carousel.click()
                expect(self.new_name_textbox).to_be_editable()
                self.new_name_textbox.fill(CHAT_FLOW_CAROUSEL_NAME[i])
                self.new_name_textbox.press("Enter")
                expect(self.kaiwa_text_list).to_contain_text(CHAT_FLOW_CAROUSEL_NAME[i], timeout=WAITING_TIMEOUT_MS)
                # Setting title
                self.react_content_cards.nth(i).locator("input[placeholder='タイトル']").fill(f"Test Carousel{i+1} Title")
                self.react_content_cards.nth(i).locator("input[placeholder='タイトル']").press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_CAROUSEL)).to_be_visible(timeout=WAITING_TIMEOUT_MS)




    # ==================================================================
    # Verification start
    # ==================================================================        
    # --- Test create new Condition group ---
    def create_new_chat_group(self):
        """Creates a new chat group."""
        # Check if Group1 and Group2 exists, if not, create it. 
        # Because Group3's reaction depends on Group1 and Group2.
        if not self.group_list.get_by_text(GROUP_NAME_KAIWA).is_visible():
            self._create_group1_if_not_exists() # Create Group1 and Textitem1

        if not self.group_list.get_by_text(GROUP_NAME_CAROUSEL).is_visible():
            self._create_group2_if_not_exists() # Create Group2 and Carousel1

        self.add_group_button.hover()
        self.add_group_newgroup.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(GROUP_NAME_CONDITION)
        self.new_name_textbox.press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_CONDITION, exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Close popup.
        self._close_tutorials_popup_if_visible()

    # --- Test create Condition item ---
    def create_condition_item(self):
        """Create new Condition item in Chat Flow page."""  
        self.add_kaiwa_button.hover()
        self.add_kaiwa_condition_item.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(CONDITION_ITEM_NAME)
        self.new_name_textbox.press("Enter")
        expect(self.kaiwa_text_list).to_contain_text(CONDITION_ITEM_NAME, timeout=WAITING_TIMEOUT_MS)

    # --- Test setting condition ---
    def setting_condition_item(self):
        """Setting condition for Condition item."""
        self.moshi_dropdown.click() # Open もし dropdown
        self.moshi_dropdown_options.get_by_text("User key").click() # Select User key
        expect(self.moshi_dropdown).to_have_text("User key", timeout=WAITING_TIMEOUT_MS)
        self.condition_input.click()
        self.condition_input.fill(CONDITION_VALUE) # Input condition value
        self.condition_input.press("Enter")