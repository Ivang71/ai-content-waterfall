import os, requests
from waterfall import colors
from dotenv import load_dotenv

load_dotenv()

wp_endpoint = os.getenv("WP_URL")
wp_auth = (os.getenv("WP_USERNAME"), os.getenv("WP_PASSWORD"))


def publish_article(topic, article_html, meta_description):
    try:
        article_data = {
            "title": topic.capitalize(),
            "content": article_html,
            "status": "publish",
            "format": "standard",
            "meta": {
                "description": meta_description,
            },
            "featured_media": 1,
            "comment_status": "closed",
        }
        response = requests.post(wp_endpoint, auth=wp_auth, json=article_data)
        response.raise_for_status()
        print("Published " + colors.GREEN + topic + colors.RESET)
    except Exception as e:
        raise Exception(f"Error publishing {article_html[:50]}: {e}")
