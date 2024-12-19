
from .img2stringgpt4 import Img2StringGPT4

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Liên kết tên node với class của nó
NODE_CLASS_MAPPINGS = {
    "Img2StringGPT4": Img2StringGPT4,
}

# Tên hiển thị trong giao diện ComfyUI
NODE_DISPLAY_NAME_MAPPINGS = {
    "Img2StringGPT4": "Img2StringGPT4",
}

# In thông báo xác nhận rằng node đã được tải
print("\033[34mImg2StringGPT4 Node: \033[92mLoaded\033[0m")
