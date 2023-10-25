import requests, os, random, string, re, sys
from concurrent.futures import ThreadPoolExecutor
import insistent_request
from dotenv import load_dotenv

load_dotenv()

ai_url = os.getenv("IMAGE_AI_URL")
host_url = os.getenv("IMAGE_HOST_API_URL")
host_key = os.getenv("IMAGE_HOST_API_KEY")

images_folder = "../images/"


def generate_image(prompt):
    """writes image to disk, returns the file name"""
    try:
        while True:
            response = insistent_request.insistent_request(ai_url, "POST", True, json={'inputs': prompt})
            if (sys.getsizeof(response.content) > 2000): # if response more than 2KB, accept image
                break
    except Exception as e:
        raise Exception(f"Failed to generate image {prompt} {e}")

    try:
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        name = f"{prompt} {random_id}.webp"
        with open(f"{images_folder}{name}", "wb") as f:
            f.write(response.content)
    except Exception as e:
        raise Exception(f"Failed to write the file {name} for the prompt {prompt}\n{e}")
    # with open("../images.txt", "a") as f:
    #     f.write(f"\n {name} {prompt} {str(sys.getsizeof(response.content))}")
    return name


def host_image(img_name):
    """Hosts image, returns link"""
    host_params = {
        "key": host_key,
        "action": "upload",
        "format": "json"
    }
    img_path = f"{images_folder}{img_name}"
    try:
        with open(img_path, "rb") as image:
            image = {"source": (img_path, image)}
            response = requests.post(host_url, params=host_params, files=image)
            response.raise_for_status()
    except Exception as e:
        raise Exception(f"Error hosting image {img_name}\n{e}")

    os.remove(img_path)
    return response.json()["image"]["url"]


def process_description(description):
    file_name = generate_image(description)
    image_link = host_image(file_name)
    return f'<img src="{image_link}" alt="{description}" width=1024 height=1024>'


def process_images(article_text):
    image_descriptions = re.findall(r'\[([^]]+)\]', article_text) # Extract image descriptions enclosed in square brackets

    with ThreadPoolExecutor() as executor:
        img_tags = list(executor.map(process_description, image_descriptions))

    print(f"Constructed html for {article_text[:30]}")

    return re.sub(r'\[([^]]+)\]', lambda x: img_tags.pop(0), article_text) # Replace [image description] placeholders
