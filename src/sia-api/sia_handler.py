import requests

class SiaBaseHandler:
    def __init__(self, hostd_url=None, renterd_url=None, hostd_username=None, hostd_password=None, renterd_password=None):
        self.hostd_url = hostd_url
        self.renterd_url = renterd_url

        self.request_headers = {
            'Content-Type': 'application/json',
        }

        # Hostd authentication
        if hostd_username or hostd_password:
            self.hostd_auth = (f"{hostd_username}", f"{hostd_password}")
            print(self.hostd_auth)
        else:
            self.hostd_auth = None

        # Renterd authentication
        if renterd_password:
            self.renterd_auth = (f"{renterd_password}",)
        else:
            self.renterd_auth = None

    def make_request(self, url, auth, method='GET', **kwargs):
        if method == 'GET':
            return requests.get(url, auth=(auth), headers=self.request_headers, **kwargs)
        elif method == 'POST':
            return requests.post(url, auth=(auth), headers=self.request_headers, **kwargs)

class SiaHostdHandler(SiaBaseHandler):
    def get_accounts(self):
        endpoint = f"{self.hostd_url}/api/accounts"
        method = "GET"
        response = self.make_request(endpoint, self.hostd_auth, method=method)
        return response.json()

    def get_wallet_information(self):
        endpoint = f"{self.hostd_url}/api/wallet"
        method = "GET"
        response = self.make_request(endpoint, self.hostd_auth, method=method)
        return response.json()

class SiaRenterdHandler(SiaBaseHandler):
    def todo(self):
        pass


# only for quick tests
if __name__ == "__main__":
    hostd_url = ""
    hostd_username = ""
    hostd_password = ""

    hostd_handler = SiaHostdHandler(hostd_url, hostd_username=hostd_username, hostd_password=hostd_password)

    # Example usage
    host_status = hostd_handler.get_accounts()
    hostd_handler.get_wallet_information()
    print(host_status)
