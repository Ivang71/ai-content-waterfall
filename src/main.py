import asyncio, random, multiprocessing
from typing import List
from talk_to_llm import talk_to_llm
from construct_html import construct_html
from publish import publish_article  


async def async_task():
    wait = random.randint(3, 20)
    print(f'getting {wait}')
    await asyncio.sleep(wait)
    print(f"got {wait}")
    return wait


def split_array(data, num_pieces):
    avg_chunk_size = len(data) // num_pieces
    remainder = len(data) % num_pieces
    chunks = []
    start = 0

    for _ in range(num_pieces):
        chunk_size = avg_chunk_size + 1 if remainder > 0 else avg_chunk_size
        chunks.append(data[start:start + chunk_size])
        start += chunk_size
        remainder -= 1

    return chunks


async def process_topic(topic: str):
    try:
        generated_text, meta_description = await talk_to_llm(topic)
        article_html = await construct_html(generated_text)
        publish_article(topic, article_html, meta_description)

    except Exception as e:
        print(f"Did not process {topic}")
        print(e)
        with open("../unprocessed_topics.txt", "a") as f:
            f.write(f"\n{topic}")


async def process_topic_list(topic_list: List[str]):
    max_concurrent_tasks = 3
    queue = asyncio.Queue(maxsize=max_concurrent_tasks)

    async def worker():
        while True:
            topic = await queue.get()
            print(topic)
            await process_topic(topic.strip())
            queue.task_done()

    # Create worker tasks
    tasks = []
    for _ in range(max_concurrent_tasks):
        task = asyncio.create_task(worker())
        tasks.append(task)

    # Add topics to the queue
    for topic in topic_list:
        await queue.put(topic.strip())

    # Wait for all tasks in the queue to be processed
    await queue.join()

    # Cancel worker tasks
    for task in tasks:
        task.cancel()

    
def process_topic_list_in_process(topic_list):
    asyncio.run(process_topic_list(topic_list))


if __name__ == "__main__":
    with open('../topics.txt', 'r') as file:
        topics = file.readlines()
    
    processes = []
    cpu_count = multiprocessing.cpu_count()
    topic_lists = split_array(topics, cpu_count)
    
    for topic_list in topic_lists:
        process = multiprocessing.Process(target=process_topic_list, args=(topic_list,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("Done")
