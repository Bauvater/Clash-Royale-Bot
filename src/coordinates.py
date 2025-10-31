from config import REGIONS, BENCH_SIZE, FIELD_ROWS, FIELD_COLS

class CoordinateCalculator:
    def __init__(self):
        self.regions = REGIONS

    def get_shop_slot_coords(self):
        x1, y1, x2, y2 = self.regions["SHOP"]
        width = x2 - x1
        slot_width = width / 3

        slot_1_x = x1 + (slot_width / 2)
        slot_2_x = x1 + slot_width + (slot_width / 2)
        slot_3_x = x1 + (2 * slot_width) + (slot_width / 2)

        y_coord = y1 + ((y2 - y1) / 2)

        return {
            "buy_slot_1": (slot_1_x, y_coord),
            "buy_slot_2": (slot_2_x, y_coord),
            "buy_slot_3": (slot_3_x, y_coord),
        }

    def get_bench_slot_coords(self):
        x1, y1, x2, y2 = self.regions["BENCH"]
        width = x2 - x1
        slot_width = width / BENCH_SIZE

        coords = {}
        for i in range(BENCH_SIZE):
            x = x1 + (i * slot_width) + (slot_width / 2)
            y = y1 + ((y2 - y1) / 2)
            coords[f"bench_slot_{i+1}"] = (x, y)
        return coords

    def get_field_slot_coords(self):
        x1, y1, x2, y2 = self.regions["FIELD"]
        width = x2 - x1
        height = y2 - y1
        slot_width = width / FIELD_COLS
        slot_height = height / FIELD_ROWS

        coords = {}
        for row in range(FIELD_ROWS):
            for col in range(FIELD_COLS):
                x = x1 + (col * slot_width) + (slot_width / 2)
                y = y1 + (row * slot_height) + (slot_height / 2)
                coords[f"field_slot_{row}_{col}"] = (x, y)
        return coords
