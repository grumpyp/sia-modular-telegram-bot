import aiohttp
import asyncio

class SiaBaseHandler:
    def __init__(self, hostd_url=None, renterd_url=None, hostd_username=None, hostd_password=None, renterd_password=None):
        self.hostd_url = hostd_url
        self.renterd_url = renterd_url

        self.request_headers = {
            'Content-Type': 'application/json',
        }

        # Hostd authentication
        if hostd_username or hostd_password:
            self.hostd_auth = aiohttp.BasicAuth(hostd_username, hostd_password)
        else:
            self.hostd_auth = None

        # Renterd authentication
        if renterd_password:
            self.renterd_auth = aiohttp.BasicAuth(renterd_password)
        else:
            self.renterd_auth = None

    async def make_request(self, url, auth, method='GET', **kwargs):
        async with aiohttp.ClientSession(auth=auth, headers=self.request_headers) as session:
            if method == 'GET':
                async with session.get(url, **kwargs) as response:
                    return await response.json()
            elif method == 'POST':
                async with session.post(url, **kwargs) as response:
                    return await response.json()

class SiaHostdHandler(SiaBaseHandler):
    async def get_accounts(self):
        endpoint = f"{self.hostd_url}/api/accounts"
        method = "GET"
        response = await self.make_request(endpoint, self.hostd_auth, method=method)
        return response

    async def get_wallet_information(self):
        endpoint = f"{self.hostd_url}/api/wallet"
        method = "GET"
        response = await self.make_request(endpoint, self.hostd_auth, method=method)
        return response
    
    async def get_metrics_information(self):
        endpoint = f"{self.hostd_url}/api/metrics"
        method = "GET"
        response = await self.make_request(endpoint, self.hostd_auth, method=method)
        return response

    async def dismiss_alert(self, alert_id):
        endpoint = f"{self.hostd_url}/api/alerts"
        method = "POST"
        data = [alert_id]
        response = await self.make_request(endpoint, self.hostd_auth, method=method, data=data)
        return response


class SiaRenterdHandler(SiaBaseHandler):
    async def todo(self):
        pass


# only for quick tests
async def main():
    hostd_url = ""
    hostd_username = ""
    hostd_password = ""

    hostd_handler = SiaHostdHandler(hostd_url, hostd_username=hostd_username, hostd_password=hostd_password)

    # Example usage
    host_status = await hostd_handler.get_accounts()
    wallet_info = await hostd_handler.get_wallet_information()
    alerts = await hostd_handler.get_alerts()
    
    # print(host_status)
    # print(wallet_info)
    print(alerts)

if __name__ == "__main__":
    asyncio.run(main())
