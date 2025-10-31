from utils import *
from game import *
import cv2
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from config import TEMPLATE_MATCHING_CONFIDENCE, WINDOW_NAME, TEMPLATE_PATH, GAME_OVER_PATH, GAME_OVER_CONFIDENCE
from gpu import GPU
import pytesseract
from PIL import Image
import os
import numpy as np

class ReadRegion:
    def __init__(self, **regions):
        self.SHOP_ROI = regions
        self.WINDOW_NAME = WINDOW_NAME
        self.GameInfo = GameInfo()
        self.confidence = TEMPLATE_MATCHING_CONFIDENCE
        self.game_over_confidence = GAME_OVER_CONFIDENCE
        self.gpu = GPU()
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except FileNotFoundError:
            print("Tesseract not found. Please install Tesseract and update the path in read_region.py")


    def preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresh

    def read_shop(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["SHOP"]
        shop_sct = game_sct[y1:y2, x1:x2]

        if self.gpu.device.type == 'cuda':
            shop_tensor = TF.to_tensor(shop_sct).unsqueeze(0).to(self.gpu.device)
            shop_tensor = TF.rgb_to_grayscale(shop_tensor)
        else:
            gray_shop_sct = cv2.cvtColor(shop_sct, cv2.COLOR_BGR2GRAY)

        shop_characters = [None, None, None]

        for character in self.GameInfo.characters:
            template = cv2.imread(f"{TEMPLATE_PATH}/{character}.png", cv2.IMREAD_GRAYSCALE)

            if self.gpu.device.type == 'cuda':
                template_tensor = TF.to_tensor(template).unsqueeze(0).to(self.gpu.device)

                # Normalized Cross-Correlation using PyTorch
                result = F.conv2d(shop_tensor, template_tensor)
                result = result / torch.sqrt(torch.sum(shop_tensor**2)) / torch.sqrt(torch.sum(template_tensor**2))

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result.cpu().numpy())
            else:
                template_match = cv2.matchTemplate(gray_shop_sct, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_match)

            if max_val >= self.confidence:
                region_width = x2 - x1
                match_x = max_loc[0]
                if match_x < region_width / 3:
                    if shop_characters[0] == None:
                        shop_characters[0] = character
                elif match_x < 2 * region_width / 3:
                    if shop_characters[1] == None:
                        shop_characters[1] = character
                else:
                    if shop_characters[2] == None:
                        shop_characters[2] = character
        return shop_characters

    def read_bench(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["BENCH"]
        bench_sct = game_sct[y1:y2, x1:x2]
        gray_bench_sct = cv2.cvtColor(bench_sct, cv2.COLOR_BGR2GRAY)

        bench_characters = []
        for character in self.GameInfo.characters:
            template = cv2.imread(f"{TEMPLATE_PATH}/{character}.png", cv2.IMREAD_GRAYSCALE)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(gray_bench_sct, template, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= self.confidence)
            for pt in zip(*loc[::-1]):
                # Add character and its top-left coordinate
                bench_characters.append((character, (x1 + pt[0], y1 + pt[1])))

        # Sort characters by their x-coordinate to maintain a consistent order
        bench_characters.sort(key=lambda c: c[1][0])
        return bench_characters

    def read_field(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["FIELD"]
        field_sct = game_sct[y1:y2, x1:x2]
        gray_field_sct = cv2.cvtColor(field_sct, cv2.COLOR_BGR2GRAY)

        field_characters = []
        for character in self.GameInfo.characters:
            template = cv2.imread(f"{TEMPLATE_PATH}/{character}.png", cv2.IMREAD_GRAYSCALE)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(gray_field_sct, template, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= self.confidence)
            for pt in zip(*loc[::-1]):
                # Add character and its top-left coordinate
                field_characters.append((character, (x1 + pt[0], y1 + pt[1])))

        # Sort characters by their x-coordinate to maintain a consistent order
        field_characters.sort(key=lambda c: c[1][0])
        return field_characters

    def read_elixir(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["ELIXIR"]
        elixir_sct = game_sct[y1:y2, x1:x2]

        preprocessed_elixir_sct = self.preprocess_image(elixir_sct)

        try:
            # Use Tesseract to extract text
            custom_config = r'--oem 3 --psm 6 outputbase digits'
            elixir_text = pytesseract.image_to_string(preprocessed_elixir_sct, config=custom_config)

            # Clean and convert to integer
            elixir_value = int(''.join(filter(str.isdigit, elixir_text)))
            return elixir_value
        except (ValueError, pytesseract.TesseractNotFoundError):
            return 0 # Return 0 if OCR fails or the value is not a digit

    def detect_game_over(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["GAME_OVER"]
        game_over_sct = game_sct[y1:y2, x1:x2]
        gray_game_over_sct = cv2.cvtColor(game_over_sct, cv2.COLOR_BGR2GRAY)

        for template_name in self.GameInfo.game_over_templates:
            template_path = os.path.join(GAME_OVER_PATH, template_name)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

            template_match = cv2.matchTemplate(gray_game_over_sct, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_match)

            if max_val >= self.game_over_confidence:
                win = "victory" in template_name
                return True, win
        return False, False
