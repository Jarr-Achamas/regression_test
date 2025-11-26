# page_objects/chatflow_image_and_video.py
from playwright.sync_api import Page, expect, Locator
from tests.web.utils.network_helpers import deploy_and_wait_for_response
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    GROUP_NAME_IMGnVDO, IMAGE_ITEM_NAME, VIDEO_ITEM_NAME, VIDEO_LINK_URL,
    APP_JSON_DEPLOY_API
    )

class CreateImageVideo:
    """Page object for the test create Image/Video in 会話フロー screen."""
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
        self.add_kaiwa_image = page.locator("dd[rt='image']")
        self.add_kaiwa_video = page.locator("dd[rt='video']")
        self.kaiwa_text_list = page.locator(".actions")
        # For upload image item
        self.react_content_cards = page.locator("div[class='cells-frame rt-card rt-imagecard rt-image rt-video rt-audio rt-imagemap rt-flyer rt-flex']")
        self.image_item_upload_icon = self.react_content_cards.nth(0).locator("i[class='icon camera large upload-btn']")
        self.image_item_preview = self.react_content_cards.nth(0).locator("li.data.imagecard")
        # Reaction for image item
        self.react_button_add = page.locator("section[class='nodes-pane']")
        self.react_button_name_input = page.locator("input[id='input_bot_btn']")
        # For upload video by file
        self.video_item_upload_icon = self.react_content_cards.nth(1).locator("i[class='icon video large upload-btn left_b']")
        self.video_tumbnail_upload_icon1 = self.react_content_cards.nth(1).locator("i[class='icon camera large upload-btn left_t']")
        # For upload video by URL
        self.video_item_upload_url = self.react_content_cards.nth(2).locator("i[class='icon link large upload-btn']")
        self.video_item_url_input = self.react_content_cards.nth(2).get_by_placeholder("MP4動画のURL入力")
        self.video_tumbnail_upload_icon2 = self.react_content_cards.nth(2).locator("i[class='icon camera large upload-btn left_t']")
        # For textitem for verification
        self.add_kaiwa_text = page.locator("dd[rt='text']")
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
    # --- Reusable Helper Methods for Tutorials Popups ---
    def _close_tutorials_popup_if_visible(self):
        """Helper to close the tutorials popup if it is visible."""
        expect(self.tutorials_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.close_popup_button.click()
        expect(self.tutorials_popup).to_be_hidden(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for Add kaiwa items ---
    def _add_kaiwa_item(self, item_type: str, item_name: str):
        """Helper to add a kaiwa item (image or video) with the given name."""
        self.add_kaiwa_button.hover()
        if item_type == "image":
            self.add_kaiwa_image.click()
        elif item_type == "video":
            self.add_kaiwa_video.click()
        else:
            raise ValueError(f"Unsupported item_type: {item_type}")
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(item_name)
        self.new_name_textbox.press("Enter")
        expect(self.kaiwa_text_list).to_contain_text(item_name, timeout=WAITING_TIMEOUT_MS)

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
    def _upload_image_item(self, item_type: str, image_path: str, upload_locator: Locator = None):
        """Helper to upload an image from file."""
        self._upload_image_with_api_wait(
            trigger_locator=upload_locator,
            image_path=image_path,
            api_url_glob="**/api/bot/action"    
        )
        if item_type == "image":
            expect(self.image_item_preview).not_to_have_attribute(
            "style", "background-image: url(\"/images/bg_cam_1.jpg\");"
            )
        elif item_type == "video":
            pass
        else:
            raise ValueError(f"Unsupported item_type: {item_type}")



    # ==================================================================
    # Verification start
    # ==================================================================        
    # --- Test create new Image/Video group ---
    def create_new_carousel_group(self):
        """Creates a new chat group."""
        # Create Group4 for Image/Video flow
        self.add_group_button.hover()
        self.add_group_newgroup.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill(GROUP_NAME_IMGnVDO)
        self.new_name_textbox.press("Enter")
        expect(self.group_list.get_by_text(GROUP_NAME_IMGnVDO, exact=True)).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Close popup.
        self._close_tutorials_popup_if_visible()

    # --- Test create Image item ---
    def create_kaiwa_item(self):
        """Creates an Image item in Group4."""
        # Select Group4
        self.group_list.get_by_text(GROUP_NAME_IMGnVDO, exact=True).click()
        self._add_kaiwa_item("image", IMAGE_ITEM_NAME)    # Add Image item
        self._add_kaiwa_item("video", VIDEO_ITEM_NAME[0]) # Add Video item
        self._add_kaiwa_item("video", VIDEO_ITEM_NAME[1]) # Add Video item

    # --- Test add Image to 画像 item --- 
    def add_image_to_image_item(self, image_path: str):
        """Adds an image to the Image item."""
        # Upload image file for image item
        self.kaiwa_text_list.get_by_text(IMAGE_ITEM_NAME).click()
        self._upload_image_item("image", image_path=image_path, upload_locator=self.image_item_upload_icon)
        # Set reaction for image item
        self.react_button_add.get_by_text("選択式ボタンを追加").nth(0).click()
        self.react_button_name_input.fill("画像ボタン")
        self.react_button_name_input.press("Enter")

    # --- Test add Video to 動画 item .mp4 ---
    def add_video_to_video_item(self, video_path: str, image_path: str):
        """Adds a video to the Video item."""
        # Upload video file for video item
        self.kaiwa_text_list.get_by_text(VIDEO_ITEM_NAME[0]).click()
        self._upload_image_item("video", image_path=video_path, upload_locator=self.video_item_upload_icon)
        # Set reaction for video item
        self.react_button_add.get_by_text("選択式ボタンを追加").nth(1).click()
        self.react_button_name_input.fill("動画ボタン")
        self.react_button_name_input.press("Enter")
        # Upload thumbnail image for video item
        self._upload_image_item("image", image_path=image_path, upload_locator=self.video_tumbnail_upload_icon1)

    # --- Test add Video to 動画 item URL ---
    def add_video_url_to_video_item(self, image_path: str):
        """Adds a video URL to the Video item."""
        # Upload video URL for video item
        self.kaiwa_text_list.get_by_text(VIDEO_ITEM_NAME[1]).click()
        self.video_item_upload_url.click()
        self.video_item_url_input.fill(VIDEO_LINK_URL)
        # Waiting for API response to make sure video URL set successfully
        api_url_glob = "**/api/bot/action"
        with self.page.expect_response(api_url_glob, timeout=WAITING_TIMEOUT_MS * 2) as response_info:
            self.video_item_url_input.press("Enter")
        response = response_info.value
        if not response.ok:
            raise AssertionError(f"Image upload API failed with status {response.status}: {response.text()}")
        # Set reaction for video item
        self.react_button_add.get_by_text("選択式ボタンを追加").nth(2).click()
        self.react_button_name_input.fill("動画URLボタン")
        self.react_button_name_input.press("Enter")
        # Upload thumbnail image for video item
        self._upload_image_item("image", image_path=image_path, upload_locator=self.video_tumbnail_upload_icon2)

    # --- Test create new text item for verification ---
    def create_new_textitem_for_verification(self):
        """Creates a new text item for verification purpose."""
        # Create Textitem2 under Group3
        self.add_kaiwa_button.hover()
        self.add_kaiwa_text.click()
        expect(self.new_name_textbox).to_be_editable()
        self.new_name_textbox.fill("Video2:Textitem")
        self.new_name_textbox.press("Enter")
        expect(self.kaiwa_text_list).to_contain_text("Video2:Textitem", timeout=WAITING_TIMEOUT_MS)
        # Add text to Textitem2
        self.kaiwa_text_msg.last.fill("Verify next chatflow content after clicking video URL button.")
        self.kaiwa_text_msg.last.press("Enter")
        # Close popup.
        self._close_tutorials_popup_if_visible()
        expect(self.kaiwa_text_msg.last).to_have_value("Verify next chatflow content after clicking video URL button.", timeout=WAITING_TIMEOUT_MS)
    
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

