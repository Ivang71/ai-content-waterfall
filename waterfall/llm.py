import vercel_ai, logging, re, random, time
import prompts.llm_prompts as prompts
from colors import ConsoleColors
from bs4 import BeautifulSoup

vercel_ai.logger.setLevel(logging.INFO)


def request_llm(content: str) -> str:
    llm = vercel_ai.Client()
    model = "openai:gpt-3.5-turbo-16k-0613"
    params = { "maxTokens": 4096 }
    response = None
    done = False
    while not done:
        try:
            response = llm.generate(model, content + " "*random.randint(0, 200), params=params)
            done = True
        except vercel_ai.MaxRetriesExceeded as e:
            llm = vercel_ai.Client()
    return response


def table_of_content_to_string(table_of_content):
    return '\n\n'.join(f'{section["heading"]}\n{section["content"]}' for section in table_of_content)


def remove_odd_images(article):
    index = -1
    def replace_odd_images(match: re.Match):
        nonlocal index
        index += 1
        return '' if index%2==0 else match.group(0)

    return re.sub(r'\{([^}]*)\}', replace_odd_images, article)


def talk_to_llm(topic: str):
    table_of_content_prompt = prompts.get_table_of_content_prompt(topic)
    raw_table_of_content = request_llm(table_of_content_prompt)

    if re.search(r'\(.*?\)\n', raw_table_of_content): # remove (Table of Content) line
        raw_table_of_content = re.sub(r'\(.*?\)\n', '', raw_table_of_content, count=1)

    headings = re.findall(r'\((.*?)\)', raw_table_of_content)
    hints = re.findall(r'\[(.*?)\]', raw_table_of_content)

    table_of_content = [{"heading": heading.strip(), "content": content.strip()} for heading, content in zip(headings, hints)]

    for index, section in enumerate(table_of_content): # fill table of content
        section_prompt = prompts.get_section_prompt(topic, table_of_content_to_string(table_of_content), index + 1, section['heading'])
        raw_section = request_llm(section_prompt)
        section["content"] = raw_section.replace('"', '')
        print(section['content'])

    article = f"<h1>{topic}</h1>\n"
    for section in table_of_content:
        article += f"<h2>{section['heading']}</h2>\n<section>{section['content']}</section>\n\n"

    soup = BeautifulSoup(article, 'html.parser')

    for p_tag in soup.find_all('p'): # remove <p> tags with a word longer than 35 characters
        if any(len(word) > 35 for word in p_tag.text.split()):
            p_tag.decompose()

    article = str(soup)

    meta_description_prompt = prompts.get_meta_description_prompt(topic)
    raw_meta_description = request_llm(meta_description_prompt)
    meta_description = raw_meta_description.replace('"', '')

    article = remove_odd_images(article)

    return article, meta_description

