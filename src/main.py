from multiprocessing import Process, cpu_count
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
from talk_to_llm import talk_to_llm
from construct_html import construct_html
from publish import publish_article


def split_array_evenly(data, num_pieces):
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


def process_topic(topic: str):
    try:
        generated_text, meta_description = talk_to_llm(topic)
        article_html = construct_html(generated_text)
        publish_article(topic, article_html, meta_description)

    except Exception as e:
        print(f"Did not process {topic}")
        print(e)
        with open("../unprocessed_topics.txt", "a") as f:
            f.write(f"\n{topic}")


def process_topic_list(topic_list: List[str]):
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_topic, item) for item in topic_list]

    wait(futures)
Ы

if __name__ == "__main__":
    with open('../topics.txt', 'r') as file:
        topics = file.readlines()
    
    processes = []
    # cpu_count = cpu_count()
    cpu_count = 1
    topic_lists = split_array_evenly(topics, cpu_count)
    
    for topic_list in topic_lists:
        process = Process(target=process_topic_list, args=(topic_list,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("Done")
