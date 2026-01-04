import requests


class SendRequest:
    def get(self, url, header=None, data=None, json=None):
        response = requests.get(url=url, headers=header, data=data, json=json)
        return response.json()

    def post(self, url, header=None, data=None, json=None):
        response = requests.post(url=url, headers=header, data=data, json=json)
        return response.json()

    def put(self, url, header=None, data=None, json=None):
        response = requests.put(url=url, headers=header, data=data, json=json)
        return response.json()

    def delete(self, url, header=None, data=None, json=None):
        response = requests.delete(url=url, headers=header, data=data, json=json)
        return response.json()

    def send_request(self, url, method, header=None, data=None, json=None):
        method = method.lower()
        request_method = getattr(self, method)
        response = request_method(url, header, data, json)
        return response
