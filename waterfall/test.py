import vercel_ai, random, logging

vercel_ai.logger.setLevel(logging.INFO)

# prompt = f"Write a lengthy engaging and a bit humorous web article about managing relationships"
prompt = """First of all, here is some information in square brackets to help you write better. Do not use it directly, but always remember who you writing to.
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


Second, I'm working on the article on the topic How to Start Investing with Just $100. Here's what i already got:

Understanding the Basics of Investing
Introduce the concept of investing and its importance in achieving financial goals. Explain key terms such as stocks, bonds, and mutual funds.

Setting Financial Goals
Discuss the significance of setting clear financial goals before starting to invest. Provide examples of short-term and long-term financial goals.

Assessing Risk Tolerance
Explain how risk tolerance plays a crucial role in determining investment strategies. Offer methods to assess individual risk tolerance levels.

Researching Investment Options
Provide an overview of various investment options suitable for beginners with limited funds, such as index funds, exchange-traded funds (ETFs), and robo-advisors.

ETFs
Explain the concept of asset allocation and its impact on portfolio diversification. Discuss different asset classes like stocks, bonds, and cash equivalents.

Understanding Asset Allocation
Offer practical tips on building a diversified investment portfolio with just $100 by considering low-cost investments and fractional shares.

Creating a Portfolio with $100
Highlight popular online investment platforms that allow individuals to start investing with small amounts like Acorns or Betterment. Discuss their features and benefits for beginners.

Utilizing Online Investment Platforms
Guide readers on developing their own personalized investment strategy based on their financial goals, risk tolerance, time horizon, and available resources.

Developing an Investment Strategy
Explain the importance of regularly monitoring investments to track progress towards financial goals.Mention tools/apps/platforms that can be used

Monitoring Your Investments
Discuss the need for rebalancing portfolios periodically to maintain desired asset allocation.Provide guidelines for rebalancing your portfolio at regular intervals

Rebalancing Your Portfolio
Highlight the benefits of seeking advice from financial professionals, such as financial advisors or investment consultants. Discuss when it may be appropriate to consult them.

Seeking Professional Advice
Emphasize the importance of staying informed about market trends and economic developments. Recommend resources like books, websites, podcasts for further education

Staying Informed and Educated
Explain methods to track and evaluate investment performance such as calculating returns, comparing against benchmarks.Provide tools that can help in this process

Tracking and Evaluating Performance
Discuss how emotions can impact investment decisions.Give tips on how to manage emotions during market fluctuations or downturns.

Managing Emotions
Provide guidance on gradually increasing investments over time as financial circumstances improve.Suggest strategies for increasing contributions.

Scaling Up Your Investments
Summarize key points discussed throughout the article.Highlight the potential for anyone to start investing with just $100 by following a strategic approach.Encourage readers to take action towards their financial goals.

Your objective is to write out the content for the heading 1 Understanding the Basics of Investing. Make it a few paragraphs that will fit in just right in the flow of the article.
Just write out the content without any commentary or the repeating title. Do not repeat the section title.
Insert some images.
I order you to insert images in your text and wrap each paragraph in <p> tag.
When you want to insert an image, write its description in curly brackets {}, the images' description should be 5 words maximum. 
Example output: 
<p>paragraph 1</p>
 {successful person}
<p>paragraph 2</p>""" + " "*random.randint(0, 20)
params = { "maxTokens": 4096 }

client = vercel_ai.Client()
text = client.generate("openai:gpt-3.5-turbo-16k-0613", prompt, params=params)

print(text)



# import g4f, proxy

# response = g4f.ChatCompletion.create(
#     provider=g4f.Provider.Vercel,
#     model=g4f.models.gpt_35_turbo,
#     messages=[{"role": "user", "content": m}],
#     stream=True
#     # proxy=proxy.get_random_proxy()
# )  # alternative model setting

# for message in response:
#     print(message)
