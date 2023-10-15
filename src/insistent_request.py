import time, traceback
from requests import Session, Response
from proxied_session import get_proxied_session


max_retries=197
retry_interval=3


def insistent_request(url: str, method: str, use_proxy=False, **kwargs) -> Response:
    """
    Args:
        url (str): The URL to send the request to
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        use_proxy (bool): Whether to use a proxy or not
        **kwargs: Additional keyword arguments that are passed to the requests.request() function
    """
    kwargs = kwargs or {}

    session = get_proxied_session() if use_proxy else Session()

    for _ in range(max_retries):
        try:
            response = session.request(method, url, timeout=13, **kwargs)
            return response
        except TimeoutError:
            session = get_proxied_session() if use_proxy else Session()
        except Exception as e:
            print(f"Error making request {e}")
            traceback.print_exc()
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    print(f"Max retries reached. Unable to complete the request.")
    return None
    