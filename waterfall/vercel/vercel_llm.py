import vercel_ai, logging, re, random, time
import waterfall.vercel.vercel_llm_prompts as prompts
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


def table_of_contents_to_string(table_of_contents):
    return '\n\n'.join(f'{section["heading"]}\n{section["content"]}' for section in table_of_contents)


def remove_odd_images(article):
    index = -1
    def replace_odd_images(match: re.Match):
        nonlocal index
        index += 1
        return '' if index%2==0 else match.group(0)

    return re.sub(r'\{([^}]*)\}', replace_odd_images, article)


def talk_to_llm(topic: str):
    table_of_content_prompt = prompts.get_table_of_contents_prompt(topic) # get prompts
    raw_table_of_contents = request_llm(table_of_content_prompt)

    if re.search(r'\(.*?\)\n', raw_table_of_contents): # remove (Table of Contents) line
        raw_table_of_contents = re.sub(r'\(.*?\)\n', '', raw_table_of_contents, count=1)

    headings = re.findall(r'\((.*?)\)', raw_table_of_contents) # construct table of contents
    hints = re.findall(r'\[(.*?)\]', raw_table_of_contents)
    table_of_contents = [{"heading": heading.strip(), "content": content.strip()} for heading, content in zip(headings, hints)]

    # for index, section in enumerate(table_of_contents): # generate the bulk
    #     section_prompt = prompts.get_section_prompt(topic, table_of_contents_to_string(table_of_contents), index + 1, section['heading'])
    #     raw_section = request_llm(section_prompt)
    #     section["content"] = raw_section.replace('"', '')
    #     print(section['content'])

    article = '<div id="article-container"><article>' # construct html
    for section in table_of_contents:
        heading = f"<h2>{section['heading']}</h2>"
        article += f"<section id={section['heading'].lower().replace(' ', '-')} class='section'>{heading}\n{section['content']}</section>\n\n"
    article += '</article></div>'

    soup = BeautifulSoup(article, 'html.parser') # add navigation
    toc = soup.new_tag('nav')
    toc['id'] = 'toc'
    toc_heading = soup.new_tag('div')
    toc_heading.string = 'Table of Contents'
    toc.append(toc_heading)
    ul_element = soup.new_tag('ul')
    headings = soup.find_all(['h2'])
    for heading in headings:
        li_element = soup.new_tag('li')
        a_element = soup.new_tag('a', href='#' + heading.get('id'))
        a_element.string = heading.text
        li_element.append(a_element)
        ul_element.append(li_element)

    toc.append(ul_element)
    toc_rail = soup.new_tag('div')
    toc_rail['id'] = 'toc-rail'
    toc_rail.append(toc)
    article_container = soup.find(id="article-container")
    article_container.insert(0, toc_rail)

    for p_tag in soup.find_all('p'): # remove <p> tags with a word longer than 35 characters
        if any(len(word) > 35 for word in p_tag.text.split()):
            p_tag.decompose()

    article = str(soup.prettify())

    # meta_description_prompt = prompts.get_meta_description_prompt(topic) # get meta description
    # raw_meta_description = request_llm(meta_description_prompt)
    # meta_description = raw_meta_description.replace('"', '')

    article = remove_odd_images(article)

    return article, 'meta_description'


article, meta = talk_to_llm('How to retire early')
print(article)
