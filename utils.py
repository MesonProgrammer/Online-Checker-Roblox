import requests

def show_error(response: requests.Response) -> Exception:
    return Exception(f"Error occurred. Status code: {response.status_code}. Text: {response.text}")
