# page_objects/chatflow_create_chat.py
from playwright.sync_api import Page, expect
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    CHAT_FLOW_TEXT_ITEMS, GROUP_NAME_KAIWA, 
    REACTION_TEXTITEM1_NAME, 
    REACTION_TEXTITEM2_NAME, USER_ATTRIBUTE_KEY_NAME, REACTION_TEXTITEM2_ACT, 
    REACTION_TEXTITEM3_ACT, 
    APP_JSON_DEPLOY_API
    )

class CreateChat:
    """Page object for the test create chat (会話) in 会話フロー screen."""
    def __init__(self, page: Page):
        self.page = page
        # Group creation
        self.add_group_button = page.get_by_role("button", name="グループ追加")
        self.add_group_newgroup = page.locator("dd[act='group']")
        self.new_name_textbox = page.locator("li.editing").get_by_role("textbox")
        self.group_list = page.locator("ul.groups")
        # Tutorials popup
        self.tutorials_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.tutorials_popup.locator(".icon.close")
        # Action chat
        self.add_kaiwa_button = page.get_by_role("button", name="会話を追加")
        self.add_kaiwa_text = page.locator("dd[rt='text']")
        self.kaiwa_text_list = page.locator(".actions")
        self.kaiwa_text_msg = page.locator("textarea.msg.with-emoticon")
        # Action button set
        self.react_button_add = page.locator("section[class='nodes-pane']")
        self.react_button_name_input = page.locator("input[id='input_bot_btn']")
        # For textitem2 reaction setting
        self.user_attribute_key_name = page.locator("input[placeholder='ユーザの属性キー名']")
        self.next_kaiwa_action2 = page.locator("section[class='pop-inline btns-form fullscreen']")
        self.destination_conversation = page.locator("input[target_name='act']")
        self.destination_conversation_select = page.locator("span[class='autocomplete-select']")
        self.destination_conversation_ul = page.locator("ul#form-item-autocomplete")
        self.save_button = page.locator("button[id='save_btn_purple']")
        self.icon_signout = page.locator(".icon.signout")
        # For textitem3 reaction setting
        self.moji_input_ato_dropdown1 = page.get_by_role("listitem", name="判定方法", exact=True).locator("div").nth(1)
        self.pattern_option = page.get_by_text("パターン", exact=True)
        self.moji_input_ato_dropdown2 = page.get_by_role("listitem", name="方法", exact=True).locator("div").nth(1)
        self.len_1 = page.get_by_text("指定なし", exact=True)
        self.next_kaiwa_action3 = page.locator("section[class='pop-inline ipts-form']")
        # For textitem4 reaction setting
        self.react_files = page.locator("section[class='pop-inline ipts-form']")
        # Deploy button and popups
        self.deploy_button = page.get_by_role("button", name="公開する")
        self.deploy_popup = page.locator(".popup:has-text('[公開]すると、以下のfacebook page、またはLINEアカウントに反映されます。')")
        self.deploy_ok_button = self.deploy_popup.get_by_role("button", name="OK")
        self.deploy_complete_popup = page.locator(".popup:has-text('デプロイが完了しました！')")
    # ==================================================================
    

    # ==================================================================
    # Reusable Helper Methods
    # ==================================================================
    # --- Reusable Helper Methods for Popups ---
    def _close_tutorials_popup_if_visible(self):
        """Helper to close the tutorials popup if it is visible."""
        expect(self.tutorials_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.close_popup_button.click()
        expect(self.tutorials_popup).to_be_hidden(timeout=WAITING_TIMEOUT_MS)

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Test create new chat group ---
    def create_new_chat_group(self):
        """Creates a new chat group."""
        self.add_group_button.hover()
        self.add_group_newgroup.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(GROUP_NAME_KAIWA)
        self.new_name_textbox.press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_KAIWA, exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Close popup.
        self._close_tutorials_popup_if_visible()

    # --- Test create new 会話 ---
    def create_new_text_items(self):
        """Create new 4 text items."""
        for i in range(4):
            # 会話追加 (Textitem)
            self.add_kaiwa_button.hover()
            self.add_kaiwa_text.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(CHAT_FLOW_TEXT_ITEMS[i])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(CHAT_FLOW_TEXT_ITEMS[i], timeout=WAITING_TIMEOUT_MS)
            # Add text to text item
            self.kaiwa_text_msg.last.fill(CHAT_FLOW_TEXT_ITEMS[i+4])
            self.kaiwa_text_msg.last.press("Enter")
            self.close_popup_button.click()
            expect(self.kaiwa_text_msg.last).to_have_value(CHAT_FLOW_TEXT_ITEMS[i+4])

    # --- Test Set reaction for Textitem1 ---
    def setting_reaction_textitem1(self):
        """Setting a reaction to Textitem1 ."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_TEXT_ITEMS[0]).click()
        self.react_button_add.get_by_text("ボタンを追加").nth(0).click()
        self.react_button_name_input.fill(REACTION_TEXTITEM1_NAME)
        self.react_button_name_input.press("Enter")
        expect(self.react_button_add.get_by_text(REACTION_TEXTITEM1_NAME).nth(0)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test Set reaction for Textitem2 ---
    def setting_reaction_textitem2(self):
        """Setting a reaction to Textitem2 ."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_TEXT_ITEMS[1]).click()
        for i in range(2):
            self.react_button_add.get_by_text("選択式ボタンを追加").nth(1).click()
            self.react_button_name_input.fill(REACTION_TEXTITEM2_NAME[i])
            self.react_button_name_input.press("Enter")
            expect(self.react_button_add.get_by_text(REACTION_TEXTITEM2_NAME[i])).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.react_button_add.get_by_text("一括編集").nth(1).click()
        self.user_attribute_key_name.fill(USER_ATTRIBUTE_KEY_NAME)
        self.next_kaiwa_action2.get_by_text("手動で指定").click()
        self.destination_conversation.fill(REACTION_TEXTITEM2_ACT)
        self.destination_conversation_ul.get_by_text(REACTION_TEXTITEM2_ACT).last.click()
        expect(self.destination_conversation_select.get_by_text(REACTION_TEXTITEM2_ACT)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_button.click()
        expect(self.icon_signout).to_have_count(2)

    # --- Test Set reaction for Textitem3 ---
    def setting_reaction_textitem3(self):
        """Setting a reaction to Textitem3 ."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_TEXT_ITEMS[2]).click()
        self.react_button_add.get_by_text("文字入力後の設定").nth(2).click()
        self.moji_input_ato_dropdown1.click()
        self.pattern_option.click()
        expect(self.moji_input_ato_dropdown1.get_by_text("パターン")).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.moji_input_ato_dropdown2.click()
        self.len_1.click()
        expect(self.moji_input_ato_dropdown2).to_have_text("指定なし", timeout=WAITING_TIMEOUT_MS)
        self.next_kaiwa_action3.get_by_text("手動で指定").click()
        self.destination_conversation.fill(REACTION_TEXTITEM3_ACT)
        self.destination_conversation_ul.get_by_text(REACTION_TEXTITEM3_ACT).last.click()
        expect(self.destination_conversation_select.get_by_text(REACTION_TEXTITEM3_ACT)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_button.click()
        expect(self.react_button_add.get_by_text("is (len:1)")).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test Set reaction for Textitem4 ---
    def setting_reaction_textitem4(self):
        """Setting a reaction to Textitem4 ."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_TEXT_ITEMS[3]).click()
        self.react_button_add.get_by_text("ファイル受信後の設定").nth(3).click()
        self.save_button.click()
        expect(self.react_button_add.get_by_text("File")).to_be_visible(timeout=WAITING_TIMEOUT_MS)

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
