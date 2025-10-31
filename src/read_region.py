from utils import *
from game import *
import cv2
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from config import TEMPLATE_MATCHING_CONFIDENCE, WINDOW_NAME, TEMPLATE_PATH
from gpu import GPU

class ReadRegion:
    def __init__(self, **regions):
        self.SHOP_ROI = regions
        self.WINDOW_NAME = WINDOW_NAME
        self.GameInfo = GameInfo()
        self.confidence = TEMPLATE_MATCHING_CONFIDENCE
        self.gpu = GPU()


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
            template_match = cv2.matchTemplate(gray_bench_sct, template, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_match)

            if max_val >= self.confidence:
                bench_characters.append(character)
        return bench_characters

    def read_field(self):
        game_sct = capture_window(self.WINDOW_NAME)
        x1, y1, x2, y2 = self.GameInfo.regions["FIELD"]
        field_sct = game_sct[y1:y2, x1:x2]

        gray_field_sct = cv2.cvtColor(field_sct, cv2.COLOR_BGR2GRAY)

        field_characters = []

        for character in self.GameInfo.characters:
            template = cv2.imread(f"{TEMPLATE_PATH}/{character}.png", cv2.IMREAD_GRAYSCALE)
            template_match = cv2.matchTemplate(gray_field_sct, template, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(template_match)

            if max_val >= self.confidence:
                field_characters.append(character)
        return field_characters

    def read_elixir(self):
        # Placeholder for OCR implementation
        return 4 # Returning a value > 0 to allow the bot to buy units
