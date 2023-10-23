import vercel_ai, logging, re, random
import prompts.llm_prompts as prompts
from colors import ConsoleColors

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


def construct_article(table_of_content):
    return '\n\n'.join(f'{section["heading"]}\n{section["content"]}' for section in table_of_content)


def talk_to_llm(topic: str):
    table_of_content_prompt = prompts.get_table_of_content_prompt(topic)
    raw_table_of_content = request_llm(table_of_content_prompt)

    if re.search(r'\(.*?\)\n', raw_table_of_content): # remove (Table of Content) line
        raw_table_of_content = re.sub(r'\(.*?\)\n', '', raw_table_of_content, count=1)

    headings = re.findall(r'\((.*?)\)', raw_table_of_content)
    hints = re.findall(r'\[(.*?)\]', raw_table_of_content)

    table_of_content = [{"heading": heading.strip(), "content": content.strip()} for heading, content in zip(headings, hints)]

    for index, section in enumerate(table_of_content):
        section_prompt = prompts.get_section_prompt(topic, construct_article(table_of_content), index + 1, section['heading'])
        raw_section = request_llm(section_prompt)
        section["content"] = raw_section.replace('"', '')
        print(section['content'])

    article = f"<h1>{topic}</h1>\n"
    for section in table_of_content:
        article += f"<h2>{section['heading']}</h2>\n<section>{section['content']}</section>\n\n"

    # meta_description_prompt = prompts.get_meta_description_prompt(topic)
    # raw_meta_description = request_llm(meta_description_prompt)
    # meta_description = raw_meta_description.replace('"', '')

    print(ConsoleColors.RED + "$"*100)
    print(article)


talk_to_llm('How to Start Investing with Just $100')
