# test case 151~
# page_objects/coupon_function.py
from playwright.sync_api import Page, expect
from config import WAITING_TIMEOUT_MS
from tests.web.test_data import (
    CP_SEGMENT_NAME, COUPON_NAME1, COUPON_DESCRIPTION,
    COUPON_DISCOUNT_CHANGE, COUPON_NAME2, COUPON_NAME3
    )

class CouponFunction:
    """Page object for the test create coupon (クーポン) in クーポン screen."""
    def __init__(self, page: Page):
        self.page = page
        # --- User screen, create segment ---
        self.header_user_tab = page.locator("//a[@name='user_list_view']")
        self.left_menu_bar = page.locator("//section[@class='left-pane with-thumb']")
        self.left_menu_all_button = self.left_menu_bar.get_by_text("すべて", exact=True)
        self.mid_menu_bar = page.locator("//section[@class='left-pane subgroups']")
        self.segment_button = self.mid_menu_bar.locator("button[hint='セグメント追加']").get_by_text("セグメント")
        self.segment_popup = page.locator("//div[@class='wide-window']")
        self.segment_save_button = self.segment_popup.locator("button[class='icon save label']")
        self.save_popup_name_input = page.locator("input[id='filter_name']")
        # --- Access coupon screen ---
        self.three_dots_icon = page.locator("header[scope='controller']").locator("a[class='miniapps icon dots-v']")
        self.three_dots_popup = page.locator("//section[@class='popover bottom white']")
        # --- Create new coupon ---
        self.coupon_create_button = page.get_by_role("button", name="クーポン発行")
        self.coupon_create_popup = page.locator("//section[@class='popup white form coupon-edit-popup']")
        self.coupon_name_input = self.coupon_create_popup.locator("input[placeholder='クーポン名']")
        self.coupon_segment_input = self.coupon_create_popup.locator("input[placeholder='Enter を入力して保存']")
        self.coupon_segment_select = page.locator("ul#form-item-autocomplete")
        self.coupon_end_date = page.locator("input[class='dt-picker dt-picker-ipt']").last
        self.coupon_description_input = page.locator("textarea[title='詳細説明']")
        self.coupon_image_upload = page.locator('input[type="file"][name="image"]')
        self.coupon_image_popup_confirm = page.locator("section[class='popup popup-confirm']")
        self.coupon_list_view_first = page.locator(".list-view").locator("tr[i='0']")
        self.coupon_list_icon_send = self.coupon_list_view_first.locator(".icon.send")
        # --- Edit coupon ---
        self.coupon_discount_input = self.coupon_create_popup.locator("input[name='discount']")
        self.coupon_discount_jpy = self.coupon_create_popup.locator("input[data-value='JPY']")
        # --- Send coupon ---
        self.coupon_sent_popup = page.locator("section[id='coupon_priview']")
        self.coupon_sent_popup_icon_send = self.coupon_sent_popup.locator(".icon.send")
        self.coupon_sent_complete_popup = page.locator("div[class='popup window']")
        self.coupon_sent_complete_close = self.coupon_sent_complete_popup.locator("i.icon.close")
        # --- Delete coupon ---
        self.coupon_delete_icon = self.coupon_list_view_first.locator("i.icon.trash")
        self.coupon_delete_popup = page.locator("section[class='popup popup-confirm']")
        self.coupon_delete_confirm_button = self.coupon_delete_popup.get_by_role("button", name="確定")
        self.coupon_data_rows = page.locator("table.list-view tr[i]")
        # --- Search coupon ---
        self.coupon_search_input = page.locator("input[placeholder='クーポンコードまたは名前で検索']")
    # ==================================================================
    

    # ==================================================================
    # Reusable Helper Methods
    # ==================================================================
    # --- Get existing coupon row ---
    def _get_coupon_data_row_count(self) -> int:
        """
        Counts only the data rows in the coupon list, ignoring the header.
        Returns 0 if the table is empty.
        """
        return self.coupon_data_rows.count()

    # --- Create new coupon function ---
    def _create_new_coupon(self, name: str, segment: str = None, end_datetime: str = None, description: str = None, image_path: str = None):
        """Creates a new coupon with the provided details."""
        self.coupon_create_button.click()
        expect(self.coupon_create_popup).to_be_visible()
        self.coupon_name_input.fill(name)   # クーポン名
        if segment:                         # 配信セグメント
            self.coupon_segment_input.fill(segment)
            self.coupon_segment_select.get_by_text(segment).last.click()
        if end_datetime:                    # 日時指定まで有効
            self.coupon_end_date.fill(end_datetime)
        if description:                     # 詳細説明
            self.coupon_description_input.fill(description)
        if image_path:                      # 画像アップロード
            self.coupon_image_upload.set_input_files(image_path)
            expect(self.coupon_image_popup_confirm).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.coupon_image_popup_confirm.locator("button").get_by_text("確定").click()
        self.coupon_create_popup.get_by_role("button", name="保存").click()
        expect(self.coupon_create_popup).not_to_be_visible()

    # --- Delete all coupons ---
    def _delete_all_coupons	(self):
        """Helper method to delete all coupons from the list."""
        while self._get_coupon_data_row_count() > 0:
            # Always delete the first coupon in the list
            self.coupon_delete_icon.click()
            expect(self.coupon_delete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
            self.coupon_delete_confirm_button.click()
            expect(self.coupon_delete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # ==================================================================
    # Verification start
    # ==================================================================
    # --- Test create new segments ---
    def create_segment(self):
        """Create new segment in the user screen."""
        # Access user screen.
        expect(self.header_user_tab).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.header_user_tab.click()                    # ユーザ
        expect(self.left_menu_bar).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Create new segment.
        self.left_menu_all_button.click()               # すべて
        expect(self.mid_menu_bar).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.segment_button.click()                     # +セグメント
        expect(self.segment_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.segment_save_button.click()                # 保存ボタン
        expect(self.save_popup_name_input).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.save_popup_name_input.fill(CP_SEGMENT_NAME) # セグメント名
        self.save_popup_name_input.press("Enter")
        expect(self.mid_menu_bar).to_contain_text(CP_SEGMENT_NAME, timeout=WAITING_TIMEOUT_MS)

    # --- Test open coupon screen and delete all previous created coupon test data ---
    def access_coupon_screen(self):
        """Access the coupon screen."""
        self.three_dots_icon.click()
        self.three_dots_popup.get_by_text("クーポン").click()
        expect(self.coupon_create_button).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Delete all coupon before start the test
        self._delete_all_coupons	()

    # --- Test create new coupon1 ---
    def create_new_coupon1(self, end_date: str, end_datetime: str, image_path: str):
        """Creates a new coupon."""
        self._create_new_coupon(COUPON_NAME1, CP_SEGMENT_NAME, end_datetime, COUPON_DESCRIPTION, image_path)
        expect(self.coupon_list_view_first).to_contain_text(COUPON_NAME1, timeout=WAITING_TIMEOUT_MS)
        expect(self.coupon_list_view_first).to_contain_text(CP_SEGMENT_NAME, timeout=WAITING_TIMEOUT_MS)
        expect(self.coupon_list_view_first).to_contain_text(end_date, timeout=WAITING_TIMEOUT_MS)
        expect(self.coupon_list_icon_send).to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test edit unsent coupon ---
    def edit_unsent_coupon(self):
        """Verify that unsent coupon can be edited."""
        self.coupon_list_view_first.click()
        expect(self.coupon_create_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        # Change % discount
        self.coupon_discount_input.fill(COUPON_DISCOUNT_CHANGE)                 # 割引変更
        self.coupon_discount_jpy.click()                                        # Change from % to 円
        self.coupon_create_popup.get_by_role("button", name="保存").click()      # save
        expect(self.coupon_list_view_first).to_contain_text(f"{COUPON_DISCOUNT_CHANGE}JPY", timeout=WAITING_TIMEOUT_MS)

    # --- Test send unsent coupon ---
    def send_unsent_coupon(self):
        """Verify that unsent coupon can be send."""
        self.coupon_list_icon_send.click()          # send icon
        expect(self.coupon_sent_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.coupon_sent_popup_icon_send.click()    # send popup
        expect(self.coupon_sent_complete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.coupon_sent_complete_close.click()     # close popup
        expect(self.coupon_sent_complete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)

    # --- Test delete sent coupon ---
    def delete_sent_coupon(self):
        """Verify that able to delete sent coupon."""
        initial_coupon_count = self._get_coupon_data_row_count() # Get the initial count
        # Perform the delete action
        self.coupon_delete_icon.click()
        expect(self.coupon_delete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.coupon_delete_confirm_button.click()
        expect(self.coupon_delete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.coupon_data_rows).to_have_count(
            max(0, initial_coupon_count - 1), 
            timeout=WAITING_TIMEOUT_MS
        )

    # --- Test delete unsent coupon ---
    def delete_unsent_coupon(self):
        """Verify that able to delete unsent coupon."""
        self._create_new_coupon(COUPON_NAME2)
        initial_coupon_count = self._get_coupon_data_row_count() # Get the initial count
        # Perform the delete action
        self.coupon_delete_icon.click()
        expect(self.coupon_delete_popup).to_be_visible(timeout=WAITING_TIMEOUT_MS)
        self.coupon_delete_confirm_button.click()
        expect(self.coupon_delete_popup).not_to_be_visible(timeout=WAITING_TIMEOUT_MS)
        expect(self.coupon_data_rows).to_have_count(
            max(0, initial_coupon_count - 1), 
            timeout=WAITING_TIMEOUT_MS
        )

    # --- Test search coupon ---
    def search_coupon(self):
        """Verify search for a coupon."""
        self._create_new_coupon(COUPON_NAME2)
        self._create_new_coupon(COUPON_NAME3)
        # Perform search action
        self.coupon_search_input.fill(COUPON_NAME2)
        self.coupon_search_input.press("Enter")
        expect(self.coupon_list_view_first).to_contain_text(COUPON_NAME2, timeout=WAITING_TIMEOUT_MS)