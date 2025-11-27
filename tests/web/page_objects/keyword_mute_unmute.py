# page_objects/keyword_mute_unmute.py
from playwright.sync_api import Page, expect
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    KEYWORD_NAME, MUTE_KEYWORD, UNMUTE_KEYWORD,
    KW_GROUP_NAME, KW_TEXTITEM_NAME, KW_TEXTITEM_MSG, REACTION_KW_TEXTITEM_ACT,
    APP_JSON_DEPLOY_API
    )


class KeywordMuteUnmute:
    """Page object for Keyword Mute/Unmute functionality in ChatFlow."""
    def __init__(self, page: Page):
        self.page = page
        # For navigate to 自動対応 page
        self.navi_dict = page.locator("dd[msg='navi-dict'] h2[class='icon comment']")
        self.message_list_view = page.locator("table[class='list-view']")
        # For add keyword Locators
        self.add_keyword_button = page.get_by_role("button", name="新規登録")
        self.popup_dict_editor = page.locator("section[class='popup dict-editor']")
        self.keyword_input = self.popup_dict_editor.locator("textarea[placeholder^='キーワード入力']")
        self.next_action_input = self.popup_dict_editor.locator("input[placeholder='遷移先の会話']")
        self.next_action_ul = page.locator("ul#form-item-autocomplete")
        self.next_action_selected = page.locator("span[class='autocomplete-select']")
        self.save_button = self.popup_dict_editor.get_by_role("button", name="保存")
        # For add mute/unmute Locators
        self.mute_settings_button = page.get_by_role("button", name="ミュート設定")
        self.popup_mute_editor = page.locator("div[class='dict-mute-editor']")
        self.left_textarea = self.popup_mute_editor.locator(".left textarea")
        self.right_textarea = self.popup_mute_editor.locator(".right textarea")
        self.popup_mute_save_button = self.popup_mute_editor.get_by_role("button", name="保存")
        self.popup_mute_close_icon = page.locator("i.icon.close").last
        # Tutorials popup
        self.tutorials_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.tutorials_popup.locator(".icon.close")
        # Create textitem under Group1 Locators
        self.add_group_button = page.get_by_role("button", name="グループ追加")
        self.add_group_newgroup = page.locator("dd[act='group']")
        self.group_list = page.locator("ul.groups")
        self.add_kaiwa_button = page.get_by_role("button", name="会話を追加")
        self.add_kaiwa_text = page.locator("dd[rt='text']")
        self.new_name_textbox = page.locator("li.editing").get_by_role("textbox")
        self.kaiwa_text_list = page.locator(".actions")
        self.kaiwa_text_msg = page.locator("textarea.msg.with-emoticon")
        # Deploy button and popups
        self.deploy_button = page.get_by_role("button", name="公開する")
        self.deploy_popup = page.locator(".popup:has-text('[公開]すると、以下のfacebook page、またはLINEアカウントに反映されます。')")
        self.deploy_ok_button = self.deploy_popup.get_by_role("button", name="OK")
        self.deploy_complete_popup = page.locator(".popup:has-text('デプロイが完了しました！')")
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
    def _create_kw_textitem_group(self):
        """Helper to create Group1 if it does not exist."""
        if not self.group_list.get_by_text(KW_GROUP_NAME).is_visible():
            # Create Group1 if it does not exist
            self.add_group_button.hover()
            self.add_group_newgroup.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(KW_GROUP_NAME)
            self.new_name_textbox.press("Enter")
            # Close popup.
            self._close_tutorials_popup_if_visible()
            # Create Textitem1 under Group1
            self.add_kaiwa_button.hover()
            self.add_kaiwa_text.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(KW_TEXTITEM_NAME)
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(KW_TEXTITEM_NAME, timeout=WAITING_TIMEOUT_MS)
            # Add text to Textitem1
            self.kaiwa_text_msg.last.fill(KW_TEXTITEM_MSG)
            self.kaiwa_text_msg.last.press("Enter")
            # Close popup.
            self._close_tutorials_popup_if_visible()
            expect(self.kaiwa_text_msg.last).to_have_value(KW_TEXTITEM_MSG)
        expect(self.group_list.get_by_text(KW_GROUP_NAME)).to_be_visible(timeout=WAITING_TIMEOUT_MS)


    # ==================================================================
    # Main Test Methods
    # ==================================================================
    # --- Navigate to 自動対応 page ---
    def navigate_to_keyword_mute_unmute_section(self):
        """Navigates to the Keyword Mute/Unmute section in ChatFlow."""
        self._create_kw_textitem_group() # Create Group1 and Textitem1
        # Navigate to Keyword Mute/Unmute section
        self.navi_dict.click() 
        expect(self.message_list_view).to_be_visible(timeout=WAITING_TIMEOUT_MS)


    # --- Create New Keyword ---
    def add_new_keyword(self):
        """Add new Keyword."""
        self.add_keyword_button.click()
        expect(self.popup_dict_editor).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.keyword_input.fill(KEYWORD_NAME)
        self.next_action_input.first.fill(REACTION_KW_TEXTITEM_ACT)
        self.next_action_ul.get_by_text(REACTION_KW_TEXTITEM_ACT).last.click()
        expect(self.next_action_selected.get_by_text(REACTION_KW_TEXTITEM_ACT)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_button.click()
        expect(self.message_list_view.filter(has_text=KEYWORD_NAME)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Set Mute/Unmute Keywords ---
    def set_mute_unmute_keywords(self):
        """Set Mute and Unmute Keywords."""
        self.mute_settings_button.click()
        expect(self.popup_mute_editor).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.left_textarea.fill(MUTE_KEYWORD) # Set Mute Keyword
        self.right_textarea.fill(UNMUTE_KEYWORD) # Set Unmute Keyword
        self.popup_mute_save_button.click() # Save Mute/Unmute settings
        expect(self.popup_mute_editor).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Verify Mute/Unmute keywords are set correctly
        self.mute_settings_button.click()
        expect(self.left_textarea).to_have_value(MUTE_KEYWORD, timeout=WAITING_TIMEOUT_MS)
        expect(self.right_textarea).to_have_value(UNMUTE_KEYWORD, timeout=WAITING_TIMEOUT_MS)
        self.popup_mute_close_icon.click()
        expect(self.popup_mute_editor).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test Deploy and verify API call ---
    def deploy_and_verify(self):
        """Deploys the application and presses Escape after successful API call."""
        # Call the reusable helper function
        deploy_and_wait_for_response(
            page=self.page,
            deploy_button=self.deploy_button,
            deploy_popup=self.deploy_popup,
            ok_button=self.deploy_ok_button,
            deploy_complete_popup=self.deploy_complete_popup,
            url_glob=APP_JSON_DEPLOY_API
        )
        # If the helper function completes without error, press "Escape"
        # self.page.keyboard.press("Escape")
