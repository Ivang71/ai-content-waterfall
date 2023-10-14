# import csv
# import random
# import requests
# import socks
# import socket

# def read_proxies():
#     proxies = []
#     with open('../2proxies.csv', newline='') as csvfile:
#         proxy_reader = csv.reader(csvfile)
#         next(proxy_reader)
#         for row in proxy_reader:
#             proxy = {
#                 "ip": row[0].strip('"'),
#                 "port": row[7].strip('"'),
#                 "protocol": row[8].strip('"'),
#             }
#             proxies.append(proxy)
#     return proxies

# protocol_mapping = {
#     'socks4': socks.SOCKS54,
#     'socks5': socks.SOCKS54,
#     'http': socks.HTTP,
# }

# def send_request_through_proxy(url, proxy_list):
#     proxy = random.choice(proxy_list)
#     socks.set_proxy(protocol_mapping[proxy['protocol']], proxy["ip"], int(proxy["port"]))
#     try:
#         response = requests.get(url)
#         print(f"Response from {proxy['ip']}:{proxy['port']} - {response.status_code}")
#     except Exception as e:
#         print(f"Failed to connect through {proxy['ip']}:{proxy['port']}: {e}")

# if __name__ == "__main__":
#     file_path = ""
#     target_url = "https://google.com"
#     proxies = read_proxies(file_path)
#     send_request_through_proxy(target_url, proxies)





# import requests

# session = requests.Session()
# session.proxies = { 'http': 'http://51.15.23.104:3128' }
# response = session.get('https://google.com')
# print(response.text)




import aiohttp
import asyncio

async def fetch_data():
    proxy_url = "http://51.15.23.104:3128"  # Replace with your proxy address
    target_url = "http://google.com"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_url, proxy=proxy_url) as response:
                response.raise_for_status()  # Raise an exception for 4xx/5xx responses
                data = await response.text()
                print(data)
        except aiohttp.ClientResponseError as exc:
            print(f"Error: {exc}")

# Run the asynchronous function
asyncio.run(fetch_data())





