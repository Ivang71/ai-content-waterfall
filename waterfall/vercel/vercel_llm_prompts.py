prompt_base = """
First of all, here is some information in square brackets to help you write better. Do not use it directly, but always remember who you writing to.
[Use easy to understand, concise, to-the-point, clever, evocative, flowing, descriptive language that paints a vivid and unforgettable picture in readers' minds.

Target Audience: Working professionals aged 25-54, actively managing finances, interested in personal finance, investing, and saving money.

Typical Financial Situation of Target Audience:
Balanced income, looking to optimize investments, managing debt responsibly, planning for major life events such as home purchase, education, or retirement.

Readers' Financial Goals:
Balanced financial growth: Prioritizing investments for wealth accumulation, actively saving for emergencies and future goals, strategically reducing debt, planning for retirement, and aiming for overall financial stability.

Common Financial Challenges:
Navigating high living costs, managing debt burdens, limited income growth, adapting to economic uncertainties, and seeking financial knowledge for effective wealth management and investment decisions.

Specific Areas of Interest:
Investing strategies, practical budgeting techniques, smart saving methods, real estate insights, retirement planning, and tips for optimizing financial resources for long-term wealth.

Key Messages:
Empowerment Through Knowledge: Provide actionable financial insights to empower readers in making informed decisions.
Strategic Financial Planning: Stress the importance of strategic planning, encompassing budgeting, saving, investing, and debt management.
Building Wealth: Offer guidance on wealth-building strategies, emphasizing prudent investments and smart money management.
Resilience Amid Challenges: Encourage resilience in the face of financial challenges, providing practical solutions to overcome obstacles.
Long-Term Financial Security: Highlight the significance of long-term financial security, focusing on retirement planning and sustainable wealth growth.

Trends and Changes in today's world:
Explore significant financial trends, including advancements in sustainable investments, evolving cryptocurrency regulations, rising interest in digital banking, and economic shifts influencing global markets.
Discuss how these trends impact personal finance, offering practical advice for adapting to the changing financial landscape.]
"""




titles_prompt = """
Make up short, catchy investopedia styles headlines for financial articles.
Make them fluid like these examples and with no colons:
"Homes Have Somehow Gotten Even Less Affordable"
"Best Robo-Advisors 2023"
"Young Investors Are Waiting for Major Life Milestones to Seek Financial Advisors"

No exclamation marks.
Generate in the following order:
1 Guides & How-To
2 Questions
3 Listicles
4 Other
Then repeat the cycle and start with 1.

Write out 100 of them in double quotes
"""




def get_table_of_contents_prompt(topic: str) -> str:
    return f"""{prompt_base}

Write a table of contents for a lengthy article on the topic {topic}. Write to conclusion. The headings should follow natural flow.
No clarifications, no introduction, no title.
Write each heading in parentheses. Then in square brackets [] write what it should be about and what type of contents include: paragraph or list or something else.


Example beginning:
(Understanding the Basics of Budgeting)
[Explain fundamental budgeting concepts and importance. Include real-life examples and relatable scenarios.]

(Creating Your Personal Budget)
[Provide step-by-step instructions on creating a budget tailored to individual income and expenses. Include budgeting tools and templates.]

(Effective Budgeting Techniques)
[Explore advanced budgeting strategies. Discuss zero-based budgeting, envelope system, and 50/30/20 rule.]
"""



def get_meta_description_prompt(article_title: str) -> str:
    return f"""Write a catchy meta description for the following article title, do not write any commentary or clarifications, do not use quotes. Just the description. Article title: {article_title}"""




def get_section_prompt(topic, raw_article: str, section_number: int, section_title) -> str:
    return f"""{prompt_base}

Second, I'm working on the article on the topic {topic}. Here's what i already got:

{raw_article}

Your objective is to write out the content for the heading {section_number} {section_title}. Make it a few paragraphs that will fit in just right in the flow of the article.
Just write out the content without any commentary or the repeating title. Do not repeat the section title.
Insert some images.
I order you to insert images in your text and wrap each paragraph in <p> tag.
If you think an image would be appropriate, then include its description in curly brackets {{}}, the images' description should be 5 words maximum.
Example output: 
<p>paragraph 1</p>
 {{successful person}}
<p>paragraph 2</p>
"""





