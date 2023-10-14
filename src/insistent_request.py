import time, random, traceback, socks, csv, requests, socket


max_retries=197
retry_interval=12


proxies = []
with open('../proxies.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        proxy = {
            "ip": row[0].strip('"'),
            "port": row[7].strip('"'),
            "protocol": row[8].strip('"'),
        }
        proxies.append(proxy)

protocol_mapping = {
    'socks4': socks.SOCKS4,
    'socks5': socks.SOCKS4,
    'http': socks.HTTP,
}

def send_request_through_proxy(url, proxy_list):
    proxy = random.choice(proxy_list)
    socks.set_proxy(protocol_mapping[proxy['protocol']], proxy["ip"], int(proxy["port"]))
    try:
        response = requests.get(url)
        print(f"Response from {proxy['ip']}:{proxy['port']} - {response.status_code}")
    except Exception as e:
        print(f"Failed to connect through {proxy['ip']}:{proxy['port']}: {e}")


def insistent_request(request_function, use_proxy=False, *args, **kwargs):
    global proxies
    args = args or ()
    kwargs = kwargs or {}

    if use_proxy:
        proxy = random.choice(proxies)
        socks.set_proxy(protocol_mapping[proxy['protocol']], proxy["ip"], int(proxy["port"]))

    for _ in range(max_retries):
        try:
            print(proxy)
            response = request_function(*args, **kwargs)  
            socks.set_default_proxy()              
            return response
        except Exception as e:
            print(f"Error making request {e}")
            traceback.print_exc()
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    else:
        print(f"Max retries reached. Unable to complete the request.")
        return None
    