import time
from os import getenv
from requests import get

from luma.led_matrix.device import ws2812
from luma.core.interface.serial import spi
from luma.core.render import canvas
from PIL import ImageFont
from dotenv import load_dotenv

from FollowerReponse import FollowerResponse

_ = load_dotenv()
TOKEN = getenv("TOKEN")
API_URL = f"https://graph.facebook.com/v23.0/SpiresSocial?fields=followers_count&access_token={TOKEN}"

def get_followers() -> int:
    res = get(API_URL)
    json = res.json()

    if json["error"]:
        print("ERROR: Could not fetch follower count:")
        print(f"{json['error']['message']}")
        exit(1)

    followers = FollowerResponse(**json)

    return followers.followers_count

# --- Setup the Matrix ---
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
device = ws2812(serial, width=32, height=8, cascaded=4, rotate=0)

# --- Load a Font ---
try:
    font = ImageFont.truetype("pixelmix.ttf", 8)
except IOError:
    print("Font file not found. Using default font.")
    font = ImageFont.load_default()

# --- Main Loop ---
while True:
    with canvas(device) as draw:
        # Clear the canvas
        draw.rectangle(device.bounding_box, outline="black", fill="black")

        num_str = f"{get_followers()}"

        # Get the bounding box of the text. The (0,0) is a starting point.
        bbox = draw.textbbox((0, 0), number_str, font=font)
        # Calculate width and height from the bounding box
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position to center the number
        x_pos = (device.width - text_width) // 2
        y_pos = (device.height - text_height) // 2

        # Draw the number onto the canvas
        # Note: We use the calculated x_pos and y_pos here.
        draw.text((x_pos, y_pos), number_str, font=font, fill="white")

    time.sleep(1)

# Clear the display at the end
device.clear()


