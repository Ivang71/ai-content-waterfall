import requests, os, re
from dotenv import load_dotenv

load_dotenv('../.env')

llm_url = os.getenv("LLM_URL")


def request_llm(payload, type, topic):
    try:
        print(f"getting {type} {topic[:30]}")
        response = requests.post(llm_url, json=payload)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Error generating {type} on topic {topic}\n{e}")


def talk_to_llm(topic):
    while True:
        article = request_llm({
            "prompt": f"""[INST] Write a lengthy web article on the topic How to invest to retire early.
                                 No clarifications, no introduction, no title.
                                 The minimum length is 6000 characters.
                                 Integrate related images with descriptions enclosed in square brackets between paragraphs.
                                 For instance:
                                 text text [smiling person enjoying retirement] text text text [/INST]\n""", # \n6000 characters is the minimum
            "version": "d24902e3fa9b698cc208b5e63136c4e26e828659a9f09827ca6ec5bb83014381",
            "systemPrompt": "You are a helpful assistant.",
            "temperature": 1,
            "topP": 0.9,
            "maxTokens": 4096,
        }, "article", topic)

        if (article and re.search(r'\[.*?\]', article)):
            break

        print(f"There's a problem getting {topic}")

    while True:
        meta_description = request_llm({
            "prompt": f"write a meta description for the following article, do not write any commentary or clarifications, do not use quotes. Just the description. Article: {article}", # \n6000 characters is the minimum
            "version": "d24902e3fa9b698cc208b5e63136c4e26e828659a9f09827ca6ec5bb83014381",
            "systemPrompt": "You are a helpful assistant.",
            "temperature": 1,
            "topP": 0.9,
            "maxTokens": 256,
        }, "meta description", topic)
        
        if meta_description:
            break

    article = re.sub(r'=', '', article)
    print(f"Got article about {topic}")
    with open('../articles.txt', 'a') as file:
        file.write('\n\n\n\n' + article)

    return article, meta_description
