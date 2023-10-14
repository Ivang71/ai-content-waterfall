import requests

def fetch_proxy_list(protocol):
    response = requests.get(f'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/{protocol}.txt')
    response.raise_for_status()
    return [f'{protocol}://{line.strip()}' for line in response.text.split('\n')]

protocols = ['socks5', 'socks4', 'http']
proxies = []

for protocol in protocols:
    proxies.extend(fetch_proxy_list(protocol))
    

