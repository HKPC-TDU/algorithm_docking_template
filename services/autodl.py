import requests


class AccessService:

    def has_permission(self, token):
        url = f'https://api.autodl.com/api/v1/dev/image/private/list'
        headers = {
            'Authorization': token,
        }
        params = {
            "page_index": 1,
            "page_size": 1,
        }
        response = requests.post(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            images = response.json()
            return images['code'] == "Success"
        return False
