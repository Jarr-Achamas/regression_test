from typing import Callable
import pytest
import logging
from playwright.sync_api import Page, Error as PlaywrightError
from datetime import datetime, date, time, timedelta
from page_objects import (
    ChatflowPage, CheckClearData, CreateChat, CreateCarousel, CouponFunction, 
    CreateImageCarouselMap, CreateImageVideo, CreateConditionItem,
    KeywordMuteUnmute
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.setup
def test_clear_previous_created_data(logged_in_chatflow_page: Page):
    """
    Check and clear created data test before start run the test.
    """
    logger.info("--- Starting test: Check and Clear previous created data ---")
    check_clear_data = CheckClearData(logged_in_chatflow_page)

    test_steps = [
        (ChatflowPage(logged_in_chatflow_page).verify_ui_elements_are_visible, 
         "[1] Chatflow page loaded successfully.", 
         "[1] FAILED to verify UI elements on Chatflow page."),
        (check_clear_data.check_clear_unwanted_groups, 
         "[2] Check and Clear all previous created Groups Chatflow data.", 
         "[2] FAILED to clear Group Chatflow data"),
        (check_clear_data.check_clear_keyword_mute_unmute, 
         "[3] Check and Clear all previous created Keyword/Mute/Unmute data.", 
         "[3] FAILED to clear Keyword/Mute/Unmute data."),
        (check_clear_data.check_clear_unwanted_coupons, 
         "[4] Check and Clear all previous created Coupons data.", 
         "[4] FAILED to clear Coupon data."),
        (check_clear_data.check_clear_unwanted_segment, 
         "[5] Check and Clear all previous created Segment data.", 
         "[5] FAILED to clear Segment data."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e: # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e: # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise # IMPORTANT: Always re-raise the exception


@pytest.mark.chatflow
@pytest.mark.textitem
def test_chatflow_kaiwa(logged_in_chatflow_page: Page):
    """
    Test creating a new 会話 flow and all related reaction.
     - Verifies the UI on the chatflow page.
     - Create a new Group1.
     - Create a new textitems
     - Setting reaction for each textitem.
     - Deploy and verify.
    """
    logger.info("--- Starting test: Create new 会話 flow and reactions ---")
    create_chat_page = CreateChat(logged_in_chatflow_page)

    test_steps = [
        (create_chat_page.create_new_chat_group, 
         "[1] Created a new Group1.", 
         "[1] FAILED to create a new Group1."),
        (create_chat_page.create_new_text_items, 
         "[2] Created new 会話 (Textitem1-Textitem4).", 
         "[2] FAILED to create new text items."),
        (create_chat_page.setting_reaction_textitem1, 
         "[3] Set reaction for Textitem1: Big button.", 
         "[3] FAILED to set reaction for Textitem1."),
        (create_chat_page.setting_reaction_textitem2, 
         "[4] Set reaction for Textitem2: Multiple choice.", 
         "[4] FAILED to set reaction for Textitem2."),
        (create_chat_page.setting_reaction_textitem3, 
         "[5] Set reaction for Textitem3: Pattern matching.", 
         "[5] FAILED to set reaction for Textitem3."),
        (create_chat_page.setting_reaction_textitem4, 
         "[6] Set reaction for Textitem4: File received.", 
         "[6] FAILED to set reaction for Textitem4."),
        (create_chat_page.deploy_and_verify, 
         "[7] Deployed the chatflow successfully.", 
         "[7] FAILED to deploy the chatflow."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e: # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e: # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise # IMPORTANT: Always re-raise the exception

@pytest.mark.coupon
def test_coupon_function(logged_in_chatflow_page: Page, image_path_factory: Callable[..., str]):
    """
    Verify the Coupon page functionality.
    - Create new coupon with segment, end date, description and image.
    - Edit unsent coupon.
    - Delete unsent coupon.
    - Delete sent coupon.
    - Search coupon.
    """
    logger.info("--- Starting test: Verify the Coupon page functionality. ---")
    # --- Test Data Setup ---
    tomorrow = date.today() + timedelta(days=1)
    end_datetime_str = datetime.combine(tomorrow, time(17, 0)).strftime("%Y-%m-%d %H:%M")
    end_date_str = tomorrow.strftime("%Y-%m-%d")
    coupon_image_path = image_path_factory("coupon")
    # --- Page Object Initialization ---
    coupon_func = CouponFunction(logged_in_chatflow_page)

    test_steps = [
        (coupon_func.create_segment,
         "[1] Created a new segment.",
         "[1] FAILED to create a new segment."),
        (coupon_func.access_coupon_screen,
         "[2] Accessed the coupon screen.",
         "[2] FAILED to access the coupon screen."),
        (lambda: coupon_func.create_new_coupon1(end_date=end_date_str, end_datetime=end_datetime_str, image_path=coupon_image_path),
         "[3] Created a new coupon flow.",
         "[3] FAILED to create a new coupon flow."),
        (coupon_func.edit_unsent_coupon,
         "[4] Verify that unsent coupon can be edited.",
         "[4] FAILED to edit the unsent coupon."),
        (coupon_func.send_unsent_coupon,
         "[5] Verify that unsent coupon can be send.",
         "[5] FAILED to send the unsent coupon."),
        (coupon_func.delete_sent_coupon,
         "[6] Verify that able to delete sent coupon.",
         "[6] FAILED to delete the sent coupon."),
        (coupon_func.delete_unsent_coupon,
         "[7] Verify that able to delete unsent coupon.",
         "[7] FAILED to delete the unsent coupon."),
        (coupon_func.search_coupon,
         "[8] Verify that able to search the coupon.",
         "[8] FAILED to search the coupon."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception

@pytest.mark.chatflow
@pytest.mark.carousel
def test_chatflow_carousel(logged_in_chatflow_page: Page):
    """
    Test creating a new カルーセル flow and all related reaction.
    -  Create a new Group2.
     - Create a new carousel.
     - Setting reaction (API, Content)
    - Deploy and verify.
    """
    logger.info("--- Starting test: Test creating a new カルーセル flow and all related reaction. ---")
    create_chat_carousel = CreateCarousel(logged_in_chatflow_page)

    test_steps = [
         (create_chat_carousel.create_new_carousel2_coupon,
         "[1] Created a new coupon for using in carousel2.",
         "[1] FAILED to create a new coupon for using in carousel2."),
        (lambda: ChatflowPage(logged_in_chatflow_page).verify_ui_elements_are_visible,
         "[2] Chatflow page loaded successfully.",
         "[2] FAILED to verify UI elements on Chatflow page."),
        (create_chat_carousel.create_new_carousel_group,
         "[3] Created a new Group2.",
         "[3] FAILED to create a new Group2."),
        (create_chat_carousel.create_new_carousel_items,
         "[4] Created new カルーセル (carousel1-carousel2).",
         "[4] FAILED to create new carousel items."),
        (create_chat_carousel.setting_reaction_carousel1,
         "[5] Set reaction for carousel1.",
         "[5] FAILED to set reaction for carousel1."),
        (create_chat_carousel.setting_reaction_carousel2,
         "[6] Set reaction for carousel2.",
         "[6] FAILED to set reaction for carousel2."),
        (create_chat_carousel.create_new_textitem_for_verification,
         "[7] Created a new text item for verification purpose.",
         "[7] FAILED to create a new text item for verification purpose."),
        (create_chat_carousel.deploy_and_verify,
         "[8] Deployed the chatflow successfully.",
         "[8] FAILED to deploy the chatflow."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception

@pytest.mark.chatflow
@pytest.mark.image_carousel_map
def test_chatflow_image_carousel_map(logged_in_chatflow_page: Page, image_path_factory: Callable[..., str]):
    """
    Test creating a new イメージカルーセル flow and イメージマップ flow and all related reaction.
    - Create a new group "Group3".
    - Create a new image carousel.
      - Setting reaction for image carousel.
    - Create a new image map.
      - Setting reaction area for image map.
    - Deploy and verify.
    """
    logger.info("--- Starting test: Test creating a new イメージカルーセル flow and all related reaction. ---")
    create_image_carousel = CreateImageCarouselMap(logged_in_chatflow_page)
    
    imagemap_image_path = image_path_factory("image_map")

    test_steps = [
        (create_image_carousel.create_new_carousel_group,
         "[1] Created a new group for using in image carousel test.",
         "[1] FAILED to create a new group for using in image carousel test."),
        (create_image_carousel.create_new_image_carousel,
         "[2] Created a new イメージカルーセル chat flow.",
         "[2] FAILED to create a new イメージカルーセル chat flow."),
        (create_image_carousel.setting_reaction_imagecarousell,
         "[3] Set reaction for image carousel.",
         "[3] FAILED to set reaction for image carousel."),
        (create_image_carousel.create_new_image_map,
         "[4] Created a new イメージマップ chat flow.",
         "[4] FAILED to create a new イメージマップ chat flow."),
        (lambda: create_image_carousel.setting_area_imagemap(image_path=imagemap_image_path),
         "[5] Set reaction area for イメージマップ.",
         "[5] FAILED to Set reaction area for イメージマップ."),
        (create_image_carousel.setting_reaction_imagemap,
         "[6] Set reaction for イメージマップ.",
         "[6] FAILED to Set reaction for イメージマップ."),
        (create_image_carousel.create_new_textitem_for_verification,
         "[7] Created a new text item for verification purpose.",
         "[7] FAILED to create a new text item for verification purpose."),
        (create_image_carousel.deploy_and_verify,
         "[8] Deployed the chatflow successfully.",
         "[8] FAILED to deploy the chatflow."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception


@pytest.mark.chatflow
@pytest.mark.image_video
def test_chatflow_image_video(logged_in_chatflow_page: Page, image_path_factory: Callable[..., str]):
    """
    Test creating a new 画像＆動画 flow and all related reaction.
    -  Create a new Group4.
     - Create a new Image/Video items.
     - Setting reaction (API)
    - Deploy and verify.
    """
    logger.info("--- Starting test: Test creating a new 画像＆動画 flow and all related reaction. ---")
    create_image_video = CreateImageVideo(logged_in_chatflow_page)

    image_item_path = image_path_factory("image1")
    video_item_path = image_path_factory("video1")

    test_steps = [
        (create_image_video.create_new_carousel_group,
         "[1] Created a new Group4.",
         "[1] FAILED to create a new Group4."),
        (create_image_video.create_kaiwa_item,
         "[2] Created new 画像＆動画 items.",
         "[2] FAILED to create new 画像＆動画 items."),
        (lambda: create_image_video.add_image_to_image_item(image_path=image_item_path),
         "[3] Set reaction for Image item.",
         "[3] FAILED to set reaction for Image item."),
        (lambda: create_image_video.add_video_to_video_item(video_path=video_item_path, image_path=image_item_path),
         "[4] Set reaction for Video item.",
         "[4] FAILED to set reaction for Video item."),
        (lambda: create_image_video.add_video_url_to_video_item(image_path=image_item_path),
         "[5] Set video URL for Video item.",
         "[5] FAILED to set video URL for Video item."),
        (create_image_video.create_new_textitem_for_verification,
         "[6] Created a new text item for verification purpose.",
         "[6] FAILED to create a new text item for verification purpose."),
        (create_image_video.deploy_and_verify,
         "[7] Deployed the chatflow successfully.",
         "[7] FAILED to deploy the chatflow."),
    ]

    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception

@pytest.mark.chatflow
@pytest.mark.condition_item
def test_chatflow_condition_item(logged_in_chatflow_page: Page):
    """
    Test creating a new 条件式 flow and all related reaction.
    -  Create a new Group5.
     - Create a new Condition item.
     - 
    - Deploy and verify.
    """
    logger.info("--- Starting test: Test creating a new 条件式 flow and all related reaction. ---")
    create_condition_item = CreateConditionItem(logged_in_chatflow_page)
    test_steps = [
        (create_condition_item.create_new_chat_group,
         "[1] Created a new Group5.",
         "[1] FAILED to create a new Group5."),
        (create_condition_item.create_condition_item,
         "[2] Created new 条件式 item.",
         "[2] FAILED to create new 条件式 item."),
        (create_condition_item.setting_condition_item,
         "[3] Set condition for 条件式 item.",
         "[3] FAILED to set condition for 条件式 item."),
        (create_condition_item.deploy_and_verify,
         "[4] Deployed the chatflow successfully.",
         "[4] FAILED to deploy the chatflow."),
    ]
    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception


@pytest.mark.keyword
def test_keyword_mute_unmute(logged_in_chatflow_page: Page):
    """
    Test creating a new keyword/mute/unmute flow and all related reaction.
    - Create a new Keyword.
    - Create a Mute word.
    - Create a Unmute word.
    - Deploy and verify.
    """
    logger.info("--- Starting test: Test creating a new keyword/mute/unmute flow and all related reaction. ---")
    keyword_mute_unmute = KeywordMuteUnmute(logged_in_chatflow_page)
    test_steps = [
        (keyword_mute_unmute.navigate_to_keyword_mute_unmute_section,
         "[1] Navigated to Keyword Mute/Unmute section.",
         "[1] FAILED to navigate to Keyword Mute/Unmute section."),
        (keyword_mute_unmute.add_new_keyword,
         "[2] Created new keyword.",
         "[2] FAILED to create new keyword."),
        (keyword_mute_unmute.set_mute_unmute_keywords,
         "[3] Created Mute and Unmute keywords.",
         "[3] FAILED to create Mute and Unmute keywords."),
        (keyword_mute_unmute.deploy_and_verify,
         "[4] Deployed the chatflow successfully.",
         "[4] FAILED to deploy the chatflow."),
    ]
    for step_func, success_msg, failure_msg in test_steps:
        try:
            step_func()
            logger.info(f"Test PASSED: {success_msg}")
        except PlaywrightError as e:  # Catching specific Playwright errors is good practice
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Playwright Error Details ---\n{e}\n-------------------------------")
            raise  # Re-raise the exception to make sure Pytest marks the test as failed
        except Exception as e:  # Catch any other unexpected errors
            logger.error(f"Test FAILED: {failure_msg}")
            logger.error(f"--- Unexpected Error Details ---\n{e}\n---------------------------------")
            raise  # IMPORTANT: Always re-raise the exception
