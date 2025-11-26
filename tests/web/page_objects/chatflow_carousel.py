# page_objects/chatflow_carousel.py
from playwright.sync_api import Page, Locator, expect
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    GROUP_NAME_CAROUSEL, CHAT_FLOW_CAROUSEL_NAME, 
    REACTION_CAROUSEL1_API, REACTION_CAROUSEL1_NAME, REACTION_CAROUSEL2_NAME, CAROUSEL2_COUPON_NAME,
    APP_JSON_DEPLOY_API
    )
 
class CreateCarousel:
    """Page object for the test create Carousel (カルーセル) in 会話フロー screen."""
    def __init__(self, page: Page):
        self.page = page
        # Access coupon screen
        self.three_dots_icon = page.locator("header[scope='controller']").locator("a[class='miniapps icon dots-v']")
        self.three_dots_popup = page.locator("//section[@class='popover bottom white']")
        self.coupon_initial_screen = page.locator("//section[@class='coupons']")
        # Create new coupon
        self.create_coupon_button = page.get_by_role("button", name="クーポン発行")
        self.coupon_create_popup = page.locator("//section[@class='popup white form coupon-edit-popup']")
        self.coupon_name_input = self.coupon_create_popup.locator("input[placeholder='クーポン名']")
        self.coupon_list_view = page.locator(".list-view")
        # Access chat flow screen
        self.header_app_tab = page.locator("//a[@name='bot_edit_view']")
        # Group creation
        self.add_group_button = page.get_by_role("button", name="グループ追加")
        self.add_group_newgroup = page.locator("dd[act='group']")
        self.new_name_textbox = page.locator("li.editing").get_by_role("textbox")
        self.group_list = page.locator("ul.groups")
        # Tutorials popup
        self.tutorials_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.tutorials_popup.locator(".icon.close")
        # Action carousel
        self.add_kaiwa_button = page.get_by_role("button", name="会話を追加")
        self.add_kaiwa_carousel = page.locator("dd[rt='card']")
        self.kaiwa_text_list = page.locator(".actions")
        # For carousel1 reaction setting
        self.card_src_select = page.locator("dl[class='card-src']")
        self.react_api_input = page.locator("input[placeholder='Your API URL']")
        self.react_content_cards = page.locator("div[class='cells rt-card rt-image rt-video rt-audio rt-imagemap rt-flyer rt-imagecard rt-flex']")
        self.react_carousel1_content_lists = self.react_content_cards.nth(0).locator("> ol")     
        self.react_big_button_name_input = page.locator("input[id='input_bot_btn']")
        # For carousel2 reaction setting
        self.react_content_dropdown = page.locator("p[class='srcs src-content']").nth(1).get_by_role("button")
        self.react_content_dropdown_coupon = page.locator("ul[class='ui-dropdown-opts']").get_by_text("クーポン", exact=True)
        self.react_button_add = page.locator("//section[@class='nodes-pane']")
        self.react_button_name_input = page.locator("input[id='input_bot_btn']")
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
    def _get_carousel_count(self) -> int:
        """
        Counts only the data rows in the coupon list, ignoring the header.
        Returns 0 if the table is empty.
        """
        return self.react_carousel1_content_lists.count()

    # --- Reusable Helper Methods for Popups ---
    def _close_tutorials_popup_if_visible(self):
        """Helper to close the tutorials popup if it is visible."""
        expect(self.tutorials_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.close_popup_button.click()
        expect(self.tutorials_popup).to_be_hidden(timeout=WAITING_TIMEOUT_MS)
    
    # --- Reusable Helper Methods for Waiting for API response when input API content and press enter ---
    def _wait_for_api_response_after_enter(self, url_glob: str, action_locator: Locator):
        """Helper to wait for API response after pressing Enter."""
        with self.page.expect_response(url_glob, timeout=WAITING_TIMEOUT_MS * 2) as response_info:
            action_locator.press("Enter")
        response = response_info.value
        if not response.ok:
            raise AssertionError(f"Carousel content import API failed with status {response.status}: {response.text()}")  
        # Assert that the API call was successful
        assert response.ok, f"API call to {url_glob} failed with status: {response.status}"

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Create coupon for using in carousel2 testing ---
    def create_new_carousel2_coupon(self):
        """Creates a new coupon."""
        # Access coupon screen
        self.three_dots_icon.click()
        expect(self.three_dots_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.three_dots_popup.get_by_text("クーポン").click()
        expect(self.coupon_initial_screen).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Create new coupon
        self.create_coupon_button.click()
        expect(self.coupon_create_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.coupon_name_input.fill(CAROUSEL2_COUPON_NAME)
        self.coupon_create_popup.get_by_role("button", name="保存").click()
        expect(self.coupon_list_view).to_contain_text(CAROUSEL2_COUPON_NAME, timeout=WAITING_TIMEOUT_MS)
    
    # --- Create new Group(Chatflow) ---
    def create_new_carousel_group(self):
        """Creates a new chat group."""
        # Access chat flow screen
        self.header_app_tab.click()
        self._close_tutorials_popup_if_visible()
        # Create Group2
        self.add_group_button.hover()
        self.add_group_newgroup.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(GROUP_NAME_CAROUSEL)
        self.new_name_textbox.press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_CAROUSEL, exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Close popup.
        self._close_tutorials_popup_if_visible()

    # --- Create Carousels ---
    def create_new_carousel_items(self):
        """Create new 2 carousel items."""
        for i in range(2):
            # 会話追加 (カルーセル)
            self.add_kaiwa_button.hover()
            self.add_kaiwa_carousel.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(CHAT_FLOW_CAROUSEL_NAME[i])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(CHAT_FLOW_CAROUSEL_NAME[i], timeout=WAITING_TIMEOUT_MS)

    # --- Set reaction for carousel1 ---
    def setting_reaction_carousel1(self):
        """Setting a reaction to Carousel1."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_CAROUSEL_NAME[0]).click()
        # Setting API data source for carousel item
        self.card_src_select.nth(0).get_by_text("API").click()
        self.react_api_input.nth(0).fill(REACTION_CAROUSEL1_API)
        # Wait for the API response after pressing Enter
        self._wait_for_api_response_after_enter("**/api/bot/action", self.react_api_input.nth(0))
        # Verify carousel items are displayed
        list_count = self._get_carousel_count()
        assert list_count > 2
        # Adding a button to carousel item
        self.react_content_cards.nth(0).get_by_text("ボタンを追加").nth(0).click()
        self.react_big_button_name_input.fill(REACTION_CAROUSEL1_NAME)
        self.react_big_button_name_input.press("Enter")
        for i in range(list_count-1): # Minus empty card (the last one)
            expect(self.react_content_cards.nth(0).get_by_text(REACTION_CAROUSEL1_NAME).nth(i)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Set reaction for carousel2 ---
    def setting_reaction_carousel2(self):
        """Setting a reaction to Carousel2."""
        self.kaiwa_text_list.get_by_text(CHAT_FLOW_CAROUSEL_NAME[1]).click()
        # Setting コンテンツ data source
        self.card_src_select.nth(1).get_by_text("コンテンツ").click()
        self.react_content_dropdown.click()
        self.react_content_dropdown_coupon.click()
        expect(self.react_content_cards.nth(1).locator(f"input[data-value='{CAROUSEL2_COUPON_NAME}']").last).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Adding a button to carousel item
        self.react_button_add.get_by_text("選択式ボタンを追加").nth(1).click()
        self.react_button_name_input.fill(REACTION_CAROUSEL2_NAME)
        self.react_button_name_input.press("Enter")
        expect(self.react_button_add.get_by_text(REACTION_CAROUSEL2_NAME)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

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