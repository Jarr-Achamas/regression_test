# page_objects/chatflow_image_carousel.py
from playwright.sync_api import Page, expect, Locator
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    GROUP_NAME_IMAGECAROUSEL, IMAGE_CAROUSEL_NAME, IMAGE_MAP_NAME, 
    REACTION_IMGCAROUSEL_API, REACTION_IMGCAROUSEL_BTN_NAME, 
    GROUP_NAME_KAIWA, CHAT_FLOW_TEXT_ITEMS, GROUP_NAME_CAROUSEL, CHAT_FLOW_CAROUSEL_NAME,
    APP_JSON_DEPLOY_API
    )
 
class CreateImageCarouselMap:
    """Page object for the test create Image Carousel (イメージカルーセル) and Image Map (イメージマップ) in 会話フロー screen."""
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
        # Action carousel
        self.add_kaiwa_button = page.get_by_role("button", name="会話を追加")
        self.add_kaiwa_imagecarousel = page.locator("dd[rt='imagecard']")
        self.add_kaiwa_imagemap= page.locator("dd[rt='imagemap']")
        self.kaiwa_text_list = page.locator(".actions")
        # For image carousel reaction setting
        self.card_src_select = page.locator("dl[class='card-src']")
        self.react_api_input = page.locator("input[placeholder='Your API URL']")
        self.react_content_cards = page.locator("div[class='cells rt-card rt-image rt-video rt-audio rt-imagemap rt-flyer rt-imagecard rt-flex']")
        self.react_content_cards_title = self.react_content_cards.last.locator("input[placeholder='タイトル']")
        self.react_carousel1_content_lists = self.react_content_cards.nth(0).locator("> ol")     
        self.react_big_button_name_input = page.locator("input[id='input_bot_btn']")
        # For image map draw area
        self.image_map_card = self.react_content_cards.last.locator("> ol")
        self.image_map_upload_icon = self.image_map_card.locator("i[class='icon camera large upload-btn']")
        self.image_map_preview = self.image_map_card.locator("li.data.imagecard")
        self.image_map_brush_icon = self.image_map_card.locator("i[class='icon brush large upload-btn']")
        self.image_map_image_area = page.locator("div[class='image-pane']")
        self.image_area = page.locator("div[class='imagemap']")
        self.image_area_save_button = page.get_by_role("button", name="保存")
        # For image map area reaction setting
        self.image_map_react_button = page.locator("div[class='react-btns']")
        self.image_map_react_popup = page.locator("section[class='pop-inline btns-form']")
        self.next_kaiwa_action = page.locator("div[class='form-type-radio']").nth(1)
        self.destination_conversation = page.locator("input[target_name='act']")
        self.destination_conversation_select = page.locator("span[class='autocomplete-select']")
        self.destination_conversation_ul = page.locator("ul#form-item-autocomplete")
        self.save_button = page.locator("button[id='save_btn_purple']")
        self.icon_signout = page.locator(".icon.signout")
        # For textitem reaction setting
        self.add_kaiwa_text = page.locator("dd[rt='text']")
        self.kaiwa_text_msg = page.locator("textarea.msg.with-emoticon")
        self.add_kaiwa_carousel = page.locator("dd[rt='card']")
        # Deploy button and popups
        self.deploy_button = page.get_by_role("button", name="公開する")
        self.deploy_popup = page.locator(".popup:has-text('[公開]すると、以下のfacebook page、またはLINEアカウントに反映されます。')")
        self.deploy_ok_button = self.deploy_popup.get_by_role("button", name="OK")
        self.deploy_complete_popup = page.locator(".popup:has-text('デプロイが完了しました！')")
    # ==================================================================
        
    # ==================================================================
    # Reusable Helper Methods
    # ==================================================================
    # --- Reusable Helper Methods for Carousel ---    
    def _get_carousel_count(self) -> int:
        """
        Counts only the data rows in the coupon list, ignoring the header.
        Returns 0 if the table is empty.
        """
        return self.react_carousel1_content_lists.count()

    # --- Reusable Helper Methods for Image Map from API ---
    def _upload_image_with_api_wait(self, trigger_locator: Locator, image_path: str, api_url_glob: str):
        """Helper to upload an image and wait for the corresponding API call to succeed."""
        with self.page.expect_file_chooser() as fc_info:
            trigger_locator.click()
        file_chooser = fc_info.value

        # Waiting for API response to make sure image uploaded successfully
        with self.page.expect_response(api_url_glob, timeout=WAITING_TIMEOUT_MS * 2) as response_info:
            file_chooser.set_files(image_path)

        response = response_info.value
        if not response.ok:
            raise AssertionError(f"Image upload API failed with status {response.status}: {response.text()}")

    # --- Reusable Helper Methods for Image Map ---
    def _upload_image_map(self, image_path: str):
        """Helper to upload an image from file."""
        self._upload_image_with_api_wait(
            trigger_locator=self.image_map_upload_icon,
            image_path=image_path,
            api_url_glob="**/api/bot/action"
        )
        # Final verification that the UI updated
        expect(self.image_map_preview).not_to_have_attribute(
            "style", "background-image: url(\"/images/bg_cam_1.jpg\");"
        )

    # --- Reusable Helper Methods for Image Map drawing area ---
    def _draw_area_on_image(self, start_x: int, start_y: int, end_x: int, end_y: int, area_name: str):
        """Helper to draw an area on the image map."""
        # Draw areas on image
        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(end_x, end_y)
        self.page.mouse.up()
        expect(self.page.locator(f"input[data-value='{area_name}']")).to_be_editable(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for Tutorials Popups ---
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
            self.add_kaiwa_button.hover()
            self.add_kaiwa_carousel.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(CHAT_FLOW_CAROUSEL_NAME[0])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(CHAT_FLOW_CAROUSEL_NAME[0], timeout=WAITING_TIMEOUT_MS)
            # Setting title for Carousel1
            self.react_content_cards_title.nth(0).fill("Test Carousel1 Title")
            self.react_content_cards_title.nth(0).press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_CAROUSEL)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for Deploy and verify ---
    def _deploy_and_verify(self):
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
        self.page.mouse.click(10, 10)
        # If the helper function completes without error, press "Escape"
        # self.page.keyboard.press("Escape")

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Test create new Carousel group ---
    def create_new_carousel_group(self):
        """Creates a new chat group."""
        # Check if Group1 and Group2 exists, if not, create it. 
        # Because Group3's reaction depends on Group1 and Group2.
        if not self.group_list.get_by_text(GROUP_NAME_KAIWA).is_visible():
            self._create_group1_if_not_exists() # Create Group1 and Textitem1
            # self._deploy_and_verify() # Call the reusable helper function
        if not self.group_list.get_by_text(GROUP_NAME_CAROUSEL).is_visible():
            self._create_group2_if_not_exists() # Create Group2 and Carousel1
            # self._deploy_and_verify() # Call the reusable helper function
        # Create Group3
        self.add_group_button.hover()
        self.add_group_newgroup.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(GROUP_NAME_IMAGECAROUSEL)
        self.new_name_textbox.press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_IMAGECAROUSEL, exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Close popup.
        self._close_tutorials_popup_if_visible()
    
    # --- Test create new イメージカルーセル ---
    def create_new_image_carousel(self):
        """Creates a new イメージカルーセル."""
        for i in range(1):
            # 会話追加 (イメージカルーセル)
            self.add_kaiwa_button.hover()
            self.add_kaiwa_imagecarousel.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(IMAGE_CAROUSEL_NAME[i])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(IMAGE_CAROUSEL_NAME[i], timeout=WAITING_TIMEOUT_MS)

    # --- Test create reaction for イメージカルーセル ---
    def setting_reaction_imagecarousell(self):
        """Setting a reaction to image carousel."""
        # Setting API data source for carousel item
        self.card_src_select.nth(0).get_by_text("API").click()
        self.react_api_input.nth(0).fill(REACTION_IMGCAROUSEL_API)
        self.react_api_input.nth(0).press("Enter")
        list_count = self._get_carousel_count()
        assert list_count > 2
        # Adding a button to carousel item
        self.react_content_cards.nth(0).get_by_text("ボタンを追加").nth(0).click()
        self.react_big_button_name_input.fill(REACTION_IMGCAROUSEL_BTN_NAME)
        self.react_big_button_name_input.press("Enter")
        for i in range(list_count-1): # Minus empty card (the last one)
            expect(self.react_content_cards.nth(0).get_by_text(REACTION_IMGCAROUSEL_BTN_NAME).nth(i)).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test create new イメージマップ ---
    def create_new_image_map(self):
        """Creates a new イメージマップ."""
        for i in range(1):
            # 会話追加 (イメージマップ)
            self.add_kaiwa_button.hover()
            self.add_kaiwa_imagemap.click()
            expect(self.new_name_textbox).to_be_editable()
            self.new_name_textbox.fill(IMAGE_MAP_NAME[i])
            self.new_name_textbox.press("Enter")
            expect(self.kaiwa_text_list).to_contain_text(IMAGE_MAP_NAME[i], timeout=WAITING_TIMEOUT_MS)

    # --- Test draw area for イメージマップ ---
    def setting_area_imagemap(self, image_path: str):
        """Sets the reaction for the image map by uploading an image."""
        # Upload image for image map
        self._upload_image_map(image_path=image_path)
        # Setting reaction for image map
        self.image_map_brush_icon.click()
        expect(self.image_map_image_area).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        image_area_box = self.image_area.bounding_box() # Draw areas on image
        assert image_area_box is not None, "Image area bounding box is None"
        start_x = image_area_box["x"] # Get the position and size of the element
        start_y = image_area_box["y"] # Get the position and size of the element
        # Draw Area 1
        self._draw_area_on_image(start_x, start_y, start_x + 233, start_y + 485, "Area 1")
        # Draw Area 2
        self._draw_area_on_image(start_x + 236, start_y, start_x + 559, start_y + 240, "Area 2")
        # Draw Area 3
        self._draw_area_on_image(start_x + 236, start_y + 243, start_x + 559, start_y + 483, "Area 3")
        # Save
        self.image_area_save_button.click()
        expect(self.image_area).to_be_hidden(timeout=WAITING_TIMEOUT_MS)

    # --- Test set reaction for イメージマップ ---
    def setting_reaction_imagemap(self):
        """Setting a reaction to image map."""
        expect(self.image_map_react_button).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Setting reaction for Area 1
        self.image_map_react_button.get_by_text("Area 1").click()
        expect(self.image_map_react_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.next_kaiwa_action.get_by_text("手動で指定").click()
        self.destination_conversation.fill(CHAT_FLOW_TEXT_ITEMS[0])
        self.destination_conversation_ul.get_by_text(CHAT_FLOW_TEXT_ITEMS[0]).last.click()
        expect(self.destination_conversation_select.get_by_text(CHAT_FLOW_TEXT_ITEMS[0])).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_button.click()

        # Setting reaction for Area 2
        self.image_map_react_button.get_by_text("Area 2").click()
        expect(self.image_map_react_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.next_kaiwa_action.get_by_text("手動で指定").click()
        self.destination_conversation.fill(CHAT_FLOW_CAROUSEL_NAME[0])
        self.destination_conversation_ul.get_by_text(CHAT_FLOW_CAROUSEL_NAME[0]).last.click()
        expect(self.destination_conversation_select.get_by_text(CHAT_FLOW_CAROUSEL_NAME[0])).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_button.click()

        # Remain "次の会話" reaction for Area 3. DO NOT set it.
        # self.image_map_react_button.get_by_text("Area 3").click()
        # expect(self.image_map_react_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)

        expect(self.icon_signout).to_have_count(2)

    # --- Create new text item for verification purpose ---
    def create_new_textitem_for_verification(self):
        """Creates a new text item for verification purpose."""
        # Create Textitem2 under Group3
        self.add_kaiwa_button.hover()
        self.add_kaiwa_text.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill("Area3:Textitem")
        self.new_name_textbox.press("Enter")
        expect(self.kaiwa_text_list).to_contain_text("Area3:Textitem", timeout=WAITING_TIMEOUT_MS)
        # Add text to Textitem2
        self.kaiwa_text_msg.last.fill("Verify next chatflow content from Image Map Area 3.")
        self.kaiwa_text_msg.last.press("Enter")
        # Close popup.
        self._close_tutorials_popup_if_visible()
        expect(self.kaiwa_text_msg.last).to_have_value("Verify next chatflow content from Image Map Area 3.", timeout=WAITING_TIMEOUT_MS)

    # --- Test Deploy and verify API call ---
    def deploy_and_verify(self):
        """Deploys the application and presses Escape after successful API call."""
        # Call the reusable helper function
        self._deploy_and_verify()