import requests


    
session = requests.Session()
session.proxies = {'http': 'socks5://66.191.31.158:80'}
session.headers.update({
    "X-Forwarded-For": "66.191.31.158",  # Replace with the IP address you want to forge
})

response = session.request('GET', 'https://httpbin.org/ip')
print(response.json())
