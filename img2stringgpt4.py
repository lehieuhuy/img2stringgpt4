
import requests
from PIL import Image

class Img2StringGPT4:
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
        """
        description = self.describe_image(input_image)
        prompt = self.call_gpt4_api(api_key, description)
        return (prompt,)

    def describe_image(self, image: Image.Image) -> str:
        width, height = image.size
        avg_color = image.resize((1, 1)).getpixel((0, 0))
        return f"An image with dimensions {width}x{height} pixels and an average color of {avg_color}."

    def call_gpt4_api(self, api_key: str, description: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
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

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API call failed: {response.status_code}, {response.text}")
