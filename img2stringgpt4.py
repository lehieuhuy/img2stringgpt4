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

    def generate_prompt(self, input_image, api_key: str) -> tuple:
        """
        Xử lý ảnh và gửi yêu cầu tới GPT-4 để tạo prompt.

        Args:
            input_image (Image.Image): Ảnh đầu vào.
            api_key (str): API key của OpenAI.

        Returns:
            tuple: Prompt được tạo.
        """
        # Kiểm tra input_image có phải là đối tượng PIL.Image.Image không
        if not isinstance(input_image, Image.Image):
            raise TypeError("The provided input_image is not a valid PIL.Image.Image object.")

        # Mô tả ảnh
        description = self.describe_image(input_image)

        # Gọi API GPT-4
        prompt = self.call_gpt4_api(api_key, description)
        return (prompt,)  # Trả về dưới dạng tuple

    def describe_image(self, image):
        """
        Phân tích cơ bản để mô tả ảnh.
        """
        if not isinstance(image, Image.Image):
            raise TypeError("The provided image is not a valid PIL.Image.Image object.")

        # Lấy kích thước và màu trung bình
        width, height = image.size
        avg_color = image.resize((1, 1)).getpixel((0, 0))
        return f"An image with dimensions {width}x{height} pixels and an average color of {avg_color}."

    def call_gpt4_api(self, api_key: str, description: str) -> str:
        """
        Gọi API GPT-4 với mô tả ảnh.
        """
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

# Đăng ký node
NODE_CLASS_MAPPINGS = {
    "Img2StringGPT4": Img2StringGPT4
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Img2StringGPT4": "Img2StringGPT4",
}

# In thông báo xác nhận rằng node đã được tải
print("\033[34mImg2StringGPT4 Node: \033[92mLoaded\033[0m")
