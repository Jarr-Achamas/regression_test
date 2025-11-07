# page_objects/check_clear_data.py
from playwright.sync_api import Page, expect, Locator
from typing import Optional
from config import WAITING_TIMEOUT_MS
# from tests.web.test_data import (

#     )

class CheckClearData:
    """Page object for Check and Clear previous created data before run the test."""
    def __init__(self, page: Page):
        self.page = page
        # Tutorials popup Locators
        self.tutorials_popup = page.locator(".popup:has-text('チャットボットの会話方法を選択')")
        self.close_popup_button = self.tutorials_popup.locator(".icon.close")
        # Delete Group (Chatflow) Locators
        self.group_list_items = page.locator("section.groups > ul.groups > li")
        self.group_delete_popup = page.locator("section[class='popover right group-form']")
        self.group_delete_confirm_button = self.group_delete_popup.get_by_role("button", name="削除")
        self.group_delete_confirm_popup = page.locator("section[class='popup popup-confirm']")
        self.group_delete_yes_button = self.group_delete_confirm_popup.get_by_role("button", name="はい")
        # Access coupon screen Locators
        self.three_dots_icon = page.locator("header[scope='controller']").locator("a[class='miniapps icon dots-v']")
        self.three_dots_popup = page.locator("//section[@class='popover bottom white']")
        self.coupon_create_button = page.get_by_role("button", name="クーポン発行")
        # Delete coupon Locators
        self.coupon_list_view_first = page.locator(".list-view").locator("tr[i='0']")
        self.coupon_delete_icon = self.coupon_list_view_first.locator("i.icon.trash")
        self.coupon_delete_popup = page.locator("section[class='popup popup-confirm']")
        self.coupon_delete_confirm_button = self.coupon_delete_popup.get_by_role("button", name="確定")
        self.coupon_data_rows = page.locator("table.list-view tr[i]")
        # Access user screen Locators
        self.header_user_tab = page.locator("//a[@name='user_list_view']")
        self.left_menu_bar = page.locator("//section[@class='left-pane with-thumb']")
        self.left_menu_all_button = self.left_menu_bar.get_by_text("すべて", exact=True)
        self.mid_menu_bar = page.locator("//section[@class='left-pane subgroups']")   
        # Delete Segment Locators
        self.segment_list_items = page.locator("section > ul.filters > li.filter")
        self.segment_popup = page.locator("//div[@class='wide-window']")
        self.segment_delete_button = self.segment_popup.get_by_role("button", name="削除")
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

    # --- Reusable Helper Methods for Groups (ChatFlow) ---
    def _find_next_unwanted_group(self) -> Optional[Locator]:
        """
        Finds the first group that should be deleted.
        Returns its locator, or None if no unwanted groups are found.
        """
        groups_to_keep = {"定期配信", "アーカイブ", "デフォルトグループ"}
        # Use .all() to get a static list for the current scan
        for group_locator in self.group_list_items.all():
            group_name = group_locator.locator("h5").inner_text()
            cog_icon_exists = group_locator.locator("i.icon.cog").count() > 0

            if group_name not in groups_to_keep and cog_icon_exists:
                return group_locator  # Return the locator of the first match
        return None  # No unwanted groups were found

    # --- Reusable Helper Methods for Delete unwanted group in Chatflow ---
    def _delete_unwanted_groups(self):
        """Helper method to delete all groups not in the 'keep' list."""
        while True:
            group_to_delete = self._find_next_unwanted_group()
            if group_to_delete is None:
                # This is the exit condition: no more deletable groups were found.
                break
            
            group_name = group_to_delete.locator("h5").inner_text()
            print(f"Found unwanted group: '{group_name}'. Deleting it...")

            # Click the cog icon within that specific group's locator
            group_to_delete.locator("i.icon.cog").click()
            
            # Handle the popup confirmation
            expect(self.group_delete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.group_delete_confirm_button.click()
            expect(self.group_delete_confirm_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.group_delete_yes_button.click()
            expect(self.group_delete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)
            # Close tutorials popup
            self._close_tutorials_popup_if_visible()
        print("Finished cleaning up groups.")


    # --- Reusable Helper Methods for Delete all unwanted Coupons ---
    def delete_all_coupons(self):
        """Helper method to delete all coupons from the list."""
        while self.coupon_data_rows.count() > 0:
            # Always delete the first coupon in the list
            self.coupon_delete_icon.click()
            expect(self.coupon_delete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.coupon_delete_confirm_button.click()
            expect(self.coupon_delete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Reusable Helper Methods for delete all unwanted Segment ---
    def _delete_all_segments(self):
        """Helper method to delete all segments from the list."""
        print("Checking for existing segments to delete...")
        while self.segment_list_items.count() > 0:
            first_segment = self.segment_list_items.first
            first_segment.locator("dd.icon.edit").click() # Click on Edit icon       
            # Delete segment
            expect(self.segment_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.segment_delete_button.click()
            expect(self.segment_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)

    
    # ==================================================================
    # Main Test Methods
    # ==================================================================
    # --- Delete all unwanted groups before starting the test ---
    def check_clear_unwanted_groups(self):
        """Access the group screen and remove all unwanted groups."""
        self._delete_unwanted_groups()

    # --- Delete all unwanted coupons before starting the test ---
    def check_clear_unwanted_coupons(self):
        """Access the coupon screen and remove all unwanted coupons."""
        self.three_dots_icon.click()
        self.three_dots_popup.get_by_text("クーポン").click()
        expect(self.coupon_create_button).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Delete all unwanted coupons
        self.delete_all_coupons()

    # --- Delete all segments before starting the test ---
    def check_clear_unwanted_segment(self):
        """Access the user screen and remove all unwanted segment."""
        # Access user screen
        expect(self.header_user_tab).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.header_user_tab.click()                    # ユーザ
        expect(self.left_menu_bar).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.left_menu_all_button.click()               # すべて
        expect(self.mid_menu_bar).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Delete all segments
        self._delete_all_segments()