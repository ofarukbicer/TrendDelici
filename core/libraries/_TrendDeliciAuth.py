import json
import random
import sys
from requests import Session, get
from core import SETTINGS

class TrendDeliciAuthException(Exception):
	pass

class VerifiyEmail():
	status = ""
	email = ""
	password = ""
	genderId = ""
	expire_time = ""
	req = ""

	def __init__(self, status, email, password, genderId, expire_time, req):
		self.status =	status
		self.email = email
		self.password = password
		self.genderId = genderId
		self.expire_time = expire_time
		self.req = req

	def account_verification(self, code):
		try:
			if self.status:
				data = {
					"email": self.email,
					"password": self.password,
					"genderId": self.genderId,
					"marketingEmailsAuthorized":False,
					"conditionOfMembershipApproved":True,
					"protectionOfPersonalDataApproved":True,
					"otpCode": code
				}
				response = self.req.post('https://auth.trendyol.com/v2/signup', data=json.dumps(data))
				if response.status_code == 200:
					return response.json()
				raise TrendDeliciAuthException(f'TrendDeliciAuthException: Trendyol API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
			else:
				return "Verification code is not valid"
		except Exception as e:
			tb = sys.exc_info()[2]
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: account_verification() -> {e}').with_traceback(tb)

class TrendDeliciAuth():
	cookies = {}

	headers = {
		'authority': 'auth.trendyol.com',
		'application-id': '1',
		'storefront-id': '1',
		'culture': 'tr-TR',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
		'accept': '*/*',
		'sec-gpc': '1',
		'origin': 'https://auth.trendyol.com',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://auth.trendyol.com/static/fragment?application-id=1&storefront-id=1&culture=tr-TR&language=tr&debug=false',
		'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
	}

	req = Session()

	accounts = []
	
	proxies = {
		'http': SETTINGS["proxies"][0],
		'https': SETTINGS["proxies"][0]
	}

	def __init__(self):
		self.req.headers.update(self.headers)
		self.req.cookies.update(self.cookies)

		if SETTINGS["proxy"]:
			self.req.proxies.update(self.proxies)

	def validate_email(self, email) -> bool:
		try:
			data = { "email": email }
			response = self.req.post('https://auth.trendyol.com/validate/email', data=json.dumps(data))
			if response.status_code == 200:
				return response.json()['isValid']
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: Trendyol API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: validate_email() -> {e}').with_traceback(tb)

	def signin(self, email, password):
		try:
			json_data = {
				'email': email,
				'password': password,
			}

			response = self.req.post('https://auth.trendyol.com/login', json=json_data)
			if response.status_code == 200:
				return response.json()
			return None
		except Exception as e:
			tb = sys.exc_info()[2]
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: signin() -> {e}').with_traceback(tb)

	def signup(self, email, password) -> VerifiyEmail:
		try:
			gender = random.randint(0, 1)
			data = {
				"email": email,
				"password": password,
				"genderId": gender,
				"marketingEmailsAuthorized":False,
				"conditionOfMembershipApproved":True,
				"protectionOfPersonalDataApproved":True
			}
			response = self.req.post('https://auth.trendyol.com/v2/signup', data=json.dumps(data))
			if response.status_code == 200:
				return VerifiyEmail(True, email, password, gender, response.json()["remainingSeconds"], self.req)
			elif "remainingSeconds" not in response:
				return VerifiyEmail(False, None, None, None, None, self.req)
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: Trendyol API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise TrendDeliciAuthException(f'TrendDeliciAuthException: signup() -> {e}').with_traceback(tb)
