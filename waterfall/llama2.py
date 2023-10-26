import requests, re
from bs4 import BeautifulSoup


models = {
    '7b': 'd24902e3fa9b698cc208b5e63136c4e26e828659a9f09827ca6ec5bb83014381',
    '13b': '9dff94b1bed5af738655d4a7cbcdcde2bd503aa85c94334fe1f42af7f3dd5ee3',
    '70b': '2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf',
}


def get_last_match(pattern, s):
    matches = re.findall(pattern, s)
    if matches:
        return matches[-1]
    else:
        return None


def request_llm(payload, type, topic):
    try:
        print(f"getting {type} {topic}")
        response = requests.post('https://www.llama2.ai/api', json=payload)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Error generating {type} on topic {topic}\n{e}")


def generate_article(topic):
    while True:
        article = request_llm({
            "prompt": f"""[INST] Write a lengthy web article on the topic {topic}.
                                 No clarifications, no introduction, no title.
                                 The minimum length is 6000 characters.
                                 The article should consist of paragraphs in <p> tags and headings in <h2> tags.
                                 Integrate related images with descriptions enclosed in square brackets between paragraphs.
                                 Example output:
                                 <h2>Exploring Investment Options</h2>
                                 <p>Once you have a clear understanding of the basics and have set your financial goals, it's time to explore various investment options suitable for beginners with limited funds. While there are numerous choices available, three popular options worth considering are index funds, exchange-traded funds (ETFs), and robo-advisors.</p>
                                 [person exploring investment options]
                                 <p>Index Funds: These types of funds aim to replicate the performance of a specific market index, such as the S&amp;P 500. They offer diversification by investing in a broad range of stocks or bonds within that index. Index funds are known for their low costs and passive management style, making them an excellent choice for long-term investors seeking stable growth.</p> [/INST]\n""",
            "version": models["70b"],
            "systemPrompt": "You are a helpful assistant.",
            "temperature": 1,
            "topP": 0.9,
            "maxTokens": 4096,
        }, "article", topic)

        if article and re.search(r'\[.*?\]', article):
            break

    while True:
        meta_description = request_llm({
            "prompt": f"write a meta description for the following topic, do not write any commentary or clarifications, do not use quotes. Just the description. Topic: {topic}",
            "version": models["7b"],
            "systemPrompt": "You are a helpful assistant.",
            "temperature": 0.75,
            "topP": 0.9,
            "maxTokens": 256,
        }, "meta description", topic)

        if (meta_description):
            break

    article = re.sub(r'=', '', article)

    soup = BeautifulSoup(article, 'html.parser')

    for p_tag in soup.find_all('p'): # Find <p> tags with content less than 120 characters and replace them with <h2> tags
        if len(p_tag.text) < 120:
            new_h2_tag = soup.new_tag('h2')
            new_h2_tag.string = p_tag.text
            p_tag.replace_with(new_h2_tag)

    article = soup.prettify()

    print(f"Got article {topic}")
    with open('../articles.txt', 'a') as file:
        file.write('\n\n\n\n' + article)

    meta_description = get_last_match(r'"([^"]*)"', meta_description)
    
    return article, meta_description

