import time

def insistent_request(request_function, *args, **kwargs):
    max_retries=197
    retry_interval=12
    args = args or ()
    kwargs = kwargs or {}

    for _ in range(max_retries):
        try:
            response = request_function(*args, **kwargs)
            return response
        except Exception as e:
            print(f"An error occurred {e}")
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    else:
        print(f"Max retries reached. Unable to complete the request.")
        return None
    