import random, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO
from waterfall import proxy


def process_description(description):
    after_colon = description.split(':')[-1].strip()
    description_arr = after_colon.lower().split()
    search_term = "+".join(description_arr)

    result_count = 0
    while not result_count:
        session = proxy.get_proxied_session()
        response = session.get(f"https://unsplash.com/ngetty/v3/search/images/creative?exclude_editorial_use_only=true&exclude_nudity=true&fields=display_set%2Creferral_destinations%2Ctitle&graphical_styles=photography&page_size=28&phrase={search_term}&sort_order=best_match")
        result_count = response.json()['result_count']
        if not result_count:
            description_arr.pop()
            search_term = "+".join(description_arr)

    images_data_list = response.json()['images']

    image_data = random.choice(images_data_list)
    alt = image_data['title']
    src = image_data['display_sizes'][-1]['uri']

    response = session.get(src)
    image = Image.open(BytesIO(response.content))
    width, height = image.size

    return f'<img src="{src}" alt="{alt}" width={width} height={height}>'


def process_images(article_text):
    image_descriptions = re.findall(r'\[([^]]+)\]', article_text) # Extract image descriptions enclosed in square brackets

    with ThreadPoolExecutor() as executor:
        img_tags = list(executor.map(process_description, image_descriptions))

    print(f"Constructed html for {article_text[:30]}")

    return re.sub(r'\[([^]]+)\]', lambda x: img_tags.pop(0), article_text) # Replace [image description] placeholders

