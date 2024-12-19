import base64
import requests
from PIL import Image
from io import BytesIO
from typing import Dict, Any

# Define the node class
class GPT4ImagePromptNode:
    """
    Node sử dụng GPT-4 API để tạo prompt từ ảnh.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_image": ("IMAGE",),
                "api_key": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Custom Nodes"

    def generate_prompt(self, input_image: Image.Image, api_key: str) -> tuple:
        """
        Xử lý ảnh và gửi yêu cầu tới GPT-4 để tạo prompt.

        Args:
            input_image (Image.Image): Ảnh đầu vào.
            api_key (str): API key của OpenAI.

        Returns:
            tuple: Prompt được tạo.
        """
        # Chuyển ảnh thành chuỗi mô tả cơ bản
        image_description = self.describe_image(input_image)

        # Gửi yêu cầu tới GPT-4
        prompt = self.call_gpt4_api(api_key, image_description)

        return (prompt,)

    def describe_image(self, image: Image.Image) -> str:
        """
        Phân tích cơ bản để mô tả ảnh.
        
        Args:
            image (Image.Image): Ảnh đầu vào.
        
        Returns:
            str: Chuỗi mô tả đơn giản về ảnh.
        """
        # Ví dụ phân tích cơ bản: kích thước ảnh, màu sắc trung bình
        width, height = image.size
        avg_color = image.resize((1, 1)).getpixel((0, 0))  # Lấy màu trung bình

        description = f"An image with dimensions {width}x{height} pixels and an average color of {avg_color}."
        return description

    def call_gpt4_api(self, api_key: str, description: str) -> str:
        """
        Gọi API GPT-4 với mô tả ảnh.

        Args:
            api_key (str): API key của OpenAI.
            description (str): Mô tả ảnh.

        Returns:
            str: Prompt được tạo.
        """
        # URL của API
        url = "https://api.openai.com/v1/chat/completions"

        # Nội dung yêu cầu
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an AI specialized in generating Stable Diffusion prompts."},
                {"role": "user", "content": f"Based on this image description: {description}, create a detailed Stable Diffusion prompt to recreate the image."}
            ],
            "temperature": 0.7,
        }

        # Gửi yêu cầu tới API
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API call failed: {response.status_code}, {response.text}")

# Đăng ký node
NODE_CLASS_MAPPINGS = {
    "GPT4ImagePromptNode": GPT4ImagePromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GPT4ImagePromptNode": "GPT-4 Image Prompt Generator"
}
