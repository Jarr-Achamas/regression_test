# TEST DATA
# DEPLOY API URL GLOB
APP_JSON_DEPLOY_API = "**/app.json"
# IMAGE
IMAGES = {
    "coupon": "coupon_img.png",
    "image_map": "image_map.jpg",
    "image1": "image1.jpg",
    "video1": "video1.mp4",
    # "campaign_banner": "campaign_banner.gif"
}

# Chat flow - 会話 flow
GROUP_NAME_KAIWA = "Group1"
CHAT_FLOW_TEXT_ITEMS = [
    "Textitem1",
    "Textitem2",
    "Textitem3",
    "Textitem4",
    "Text1",
    "Text2",
    "Text3",
    "Text4"
]
REACTION_TEXTITEM1_NAME = "text1 button"
REACTION_TEXTITEM2_NAME = [
    "choice1",
    "choice2"
]
USER_ATTRIBUTE_KEY_NAME = "choice"
REACTION_TEXTITEM2_ACT = "3:Textitem3"
REACTION_TEXTITEM3_ACT = "4:Textitem4"

# Create coupon for Carousel2
CAROUSEL2_COUPON_NAME = "Carousel2Coupon"

# Chat flow - カルーセル flow
GROUP_NAME_CAROUSEL = "Group2"
CHAT_FLOW_CAROUSEL_NAME = [
    "carousel1",
    "carousel2"
]
REACTION_CAROUSEL1_API = "https://pre.bonp.me/api/service/recipes/?format=list"
REACTION_CAROUSEL1_NAME = "carousel1 button"
REACTION_CAROUSEL2_NAME = "carousel2 button"

# Coupon function verification
CP_SEGMENT_NAME = "cp-segment1"
COUPON_NAME1 = "cp-coupon1"
COUPON_NAME2 = "cp-coupon2"
COUPON_NAME3 = "cp-coupon3"
COUPON_DESCRIPTION = "Here is a description for cp-coupon1"
COUPON_DISCOUNT_CHANGE = "10"


# Image Carousel - イメージカルーセル
GROUP_NAME_IMAGECAROUSEL = "Group3"
IMAGE_CAROUSEL_NAME = [
    "image_carousel",
]
IMAGE_MAP_NAME = [
    "image_map",
]
REACTION_IMGCAROUSEL_API = "https://pre.bonp.me/api/service/recipes/?format=list"
REACTION_IMGCAROUSEL_BTN_NAME = "IMG_ボタン"

# Chat flow - 画像＆動画 flow
GROUP_NAME_IMGnVDO = "Group4"
IMAGE_ITEM_NAME = "image1"
VIDEO_ITEM_NAME = "video1"