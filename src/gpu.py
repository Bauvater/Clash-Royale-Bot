import torch

class GPU:
    def __init__(self):
        self.device = self.get_device()

    def get_device(self):
        if torch.cuda.is_available():
            print("CUDA is available! Using GPU.")
            return torch.device("cuda")
        else:
            print("CUDA not available. Using CPU.")
            return torch.device("cpu")

    def get_device_name(self):
        if self.device.type == "cuda":
            return torch.cuda.get_device_name(0)
        else:
            return "CPU"
