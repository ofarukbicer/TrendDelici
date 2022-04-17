import sys
from wsgiref import headers
from requests import Session, get
from core.libraries._TrendDeliciAuth import TrendDeliciAuth
from core.libraries._TrendDeliciProduct import TrendDeliciProduct
from core import SETTINGS

class TrendDeliciAccountException(Exception):
	pass

class TrendDeliciAccount():
	login = False
	accessToken = ""
	email = ""
	password = ""
	req = Session()
	auth = TrendDeliciAuth()

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
		'Origin': 'https://www.trendyol.com',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-site',
		'If-None-Match': 'W/"849-r9u9xixv9pBgfq4VybeyMp7+xn8"',
	}

	proxies = {
		'http': SETTINGS["proxies"][0],
		'https': SETTINGS["proxies"][0]
	}

	def __init__(self, email, password):
		self.email = email
		self.password = password
		
		self.req.headers.update(self.headers)

		if SETTINGS["proxy"]:
			self.req.proxies.update(self.proxies)

		signin = self.auth.signin(self.email, self.password)
		if signin:
			self.accessToken = signin["accessToken"]
			self.req.headers.update({"Authorization": f"Bearer {self.accessToken}"})
			self.login = True
		else:
			self.login = False
		
	def close(self):
		headers = {
			'authority': 'www.trendyol.com',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-site': 'same-origin',
			'sec-gpc': '1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
		}
		logout = get('https://trendyol.com/authentication/logout', headers=headers)
		if logout.status_code == 200:
			self.req.close()
			self.req.headers.clear()
			self.req.cookies.clear()
			self.req.proxies.clear()
			self.login = False
			return True
		raise TrendDeliciAccountException(f'TrendDeliciAccountException: Trendyol API not responding\n Status Code: {logout.status_code} -> {logout.text or logout.content}')

	def get_coupons(self) -> list:
		try:
			params = {
				'page': '1',
				'culture': 'tr-TR',
				'storefrontId': '1',
			}

			response = self.req.get('https://public-mdc.trendyol.com/discovery-web-coupongw-service/api/coupons', params=params)
			if response.status_code == 200:
				return response.json()["result"]["coupons"]
			raise TrendDeliciAccountException(f'TrendDeliciAccountException: Trendyol API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise TrendDeliciAccountException(f'TrendDeliciAccountException: get_coupons() -> {e}').with_traceback(tb)
	
	def add_favorite(self, data):
		params = {
			'storefrontId': '1',
			'culture': 'tr-TR',
		}

		add_fav = self.req.post('https://public-mdc.trendyol.com/discovery-web-recogw-service/api/favorites', params=params, json=data)
		if add_fav.status_code == 200:
			return True
		raise TrendDeliciAccountException(f'TrendDeliciAccountException: Trendyol API not responding\n Status Code: {add_fav.status_code} -> {add_fav.text or add_fav.content}')

	def follow_store(self, store_id):
		params = {
    'sellerId': store_id,
		}
		self.req.headers.update({"Authorization": f"{self.accessToken}"})

		follow_store = self.req.post('https://public-sdc.trendyol.com/discovery-sellerstore-webgw-service/v1/follow/', params=params)

		if follow_store.status_code == 201:
			self.req.headers.update({"Authorization": f"Bearer {self.accessToken}"})
			return follow_store.json()
		raise TrendDeliciAccountException(f'TrendDeliciAccountException: Trendyol API not responding\n Status Code: {follow_store.status_code} -> {follow_store.text or follow_store.content}')