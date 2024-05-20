import requests


class StripeServiceClient:

    def __init__(self, api_key):
        self.api_key = api_key

    def create_product(self, url: str, name: str):
        # url = 'https://api.stripe.com/v1/products'
        data = {
            'name': name,
        }
        response = requests.post(
            url=url,
            data=data,
            auth=(self.api_key, '')
        )
        return response.json()

    def create_price(self, url: str, name: str, price: int):
        data = {
            'currency': 'rub',
            'unit_amount': price * 100,
            'recurring[interval]': 'month',
            'product_data[name]': name
        }
        response = requests.post(
            url=url,
            data=data,
            auth=(self.api_key, '')
        )
        return response.json()

    def create_session(self, url: str, price_id: int, success_url: str):
        data = {
            'success_url': success_url,
            'line_items[0][price]': price_id,
            'line_items[0][quantity]': 1,
            'mode': 'subscription',
        }
        response = requests.post(
            url=url,
            data=data,
            auth=(self.api_key, '')
        )
        return response.json()
