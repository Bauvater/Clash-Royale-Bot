import pygetwindow as gw
import numpy as np
import mss, cv2, time, os, keyboard
from config import WINDOW_SIZE
from PIL import Image, ImageDraw, ImageFont
import shutil

def get_window_rect(title_substr):
    wins = gw.getWindowsWithTitle(title_substr)
    if not wins:
        raise RuntimeError("Window not found")
    win = wins[0]
    left, top = win.topleft
    dimensions = {
        "width": win.width,
        "height": win.height
    }
    if dimensions["width"] != WINDOW_SIZE["width"] or dimensions["height"] != WINDOW_SIZE["height"]:
        raise RuntimeError(f"Window size is not {WINDOW_SIZE['width']}x{WINDOW_SIZE['height']}")
    return {
        "left": left,
        "top": top,
        "width": win.width,
        "height": win.height
    }

def capture_window(title_substr):
    region = get_window_rect(title_substr)
    with mss.mss() as sct:
        monitor = {
            "left": region["left"],
            "top": region["top"],
            "width": region["width"],
            "height": region["height"]
        }

        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return img

def determine_roi(window_title, message="Select ROI"):
    img = capture_window(window_title)

    clicks = []
    roi_result = {}

    def click_event(event, x, y, flags, param):
        nonlocal clicks, img, roi_result
        if event == cv2.EVENT_LBUTTONDOWN:
            clicks.append((x, y))
            print(f"Clicked at: ({x}, {y})")
            if len(clicks) == 2:
                x1, y1 = clicks[0]
                x2, y2 = clicks[1]
                # Normalize ordering
                x1n, x2n = sorted((int(x1), int(x2)))
                y1n, y2n = sorted((int(y1), int(y2)))
                roi = img[y1n:y2n, x1n:x2n].copy()
                cv2.imshow("Cropped ROI", roi)
                cv2.waitKey(0)
                cv2.destroyWindow("Cropped ROI")
                roi_result["roi"] = (x1n, y1n, x2n, y2n)
                print(f"Final ROI = ({x1n}, {y1n}, {x2n}, {y2n})")
                cv2.destroyAllWindows()

    window_name = f"Select ROI - {message}"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(window_name, click_event)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if "roi" not in roi_result:
        raise RuntimeError("ROI selection cancelled or incomplete")
    return roi_result["roi"]

def screenshot_collector(roi, window_title="Bluestacks", save_dir="templates"):
    print("Press 'S' to capture region. Press 'Q' to quit.")
    os.makedirs(save_dir, exist_ok=True)
    counter = 0

    while True:
        if keyboard.is_pressed("s"):
            frame = capture_window(window_title) # captures full window
            x1, y1, x2, y2 = roi # unpacks roi
            shop_crop = frame[y1:y2, x1:x2] # crops to roi 

            filename = os.path.join(
                save_dir, 
                f"capture_{int(time.time())}_{counter}.png"
            ) # determines file name and location based on time and counter
            cv2.imwrite(filename, shop_crop) # saves file
            counter += 1 # adds one to counter
            print(f"Saved: {filename}") # prints saved file name
            time.sleep(0.3) # very simple debounce

        if keyboard.is_pressed("q"):
            print("Exiting image collector.") # prints exit message
            break # exits loop

def create_placeholder_images():
    game_over_dir = "templates/game_over"
    if os.path.exists(game_over_dir):
        shutil.rmtree(game_over_dir)
    os.makedirs(game_over_dir)

    width, height = 200, 100
    try:
        font = ImageFont.truetype("c:/Windows/Fonts/arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Victory Image
    victory_img = Image.new('RGB', (width, height), color = 'black')
    d = ImageDraw.Draw(victory_img)
    d.text((10,10), "Victory", font=font, fill=(255,255,0))
    victory_img.save(f"{game_over_dir}/victory.png")

    # Defeat Image
    defeat_img = Image.new('RGB', (width, height), color = 'black')
    d = ImageDraw.Draw(defeat_img)
    d.text((10,10), "Defeat", font=font, fill=(255,0,0))
    defeat_img.save(f"{game_over_dir}/defeat.png")

if __name__ == "__main__":
    create_placeholder_images()
