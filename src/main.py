from concurrent.futures import ThreadPoolExecutor
from talk_to_llm import talk_to_llm
from construct_html import construct_html
from publish import publish_article


def process_topic(topic):
    try:
        generated_text, meta_description = talk_to_llm(topic)
        article_html = construct_html(generated_text)
        publish_article(topic, article_html, meta_description)

    except Exception as e:
        print(f"Did not process {topic}")
        print(e)
        with open("../unprocessed_topics.txt", "a") as f:
            f.write(f"\n{topic}")


def main():
    while True:
        with open('../topics.txt', 'r') as file:
            topics = file.readlines(3)
            if not topics:
                break

            with ThreadPoolExecutor(max_workers=128) as executor:
                executor.map(process_topic, topics)


if __name__ == "__main__":
    main()
