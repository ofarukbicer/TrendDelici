import imp
import sys
from requests import post, get
import re

class KopeechkaServiceException(Exception):
	pass
	
class KopeechkaService():
	token = ""
	mails = []

	def __init__(self, token):
		self.token = token

	def get_balance(self):
		try:
			response = get(f"http://api.kopeechka.store/user-balance?token={self.token}&api=2.0")
			if response.status_code == 200:
				data = response.json()
				if data['status'] == 'OK':
					return data["balance"]
				return KopeechkaServiceException(f'KopeechkaServiceException: Failed to receive balance')
			return KopeechkaServiceException(f'KopeechkaServiceException: Kopeechka API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise KopeechkaServiceException(f'KopeechkaServiceException: get_balance() -> {e}').with_traceback(tb)

	def get_email(self, domain, mail_type = "mail.ru"):
		try:
			response = get(f"https://api.kopeechka.store/mailbox-get-email?api=2.0&spa=1&site={domain}&sender={domain.split('.')[0]}&regex=&mail_type={mail_type}&token={self.token}")
			if response.status_code == 200:
				data = response.json()
				if data['status'] == 'OK':
					self.mails.append({
						"mail": data["mail"],
						"id": data["id"],
					})
					return {
						"mail": data["mail"],
						"id": data["id"],
					}
				return KopeechkaServiceException(f'KopeechkaServiceException: Failed to receive email')
			return KopeechkaServiceException(f'KopeechkaServiceException: Kopeechka API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise KopeechkaServiceException(f'KopeechkaServiceException: get_email() -> {e}').with_traceback(tb)

	def get_verification_code(self, id):
		try:
			response = get(f"https://api.kopeechka.store/mailbox-get-message?full=1&spa=1&id={id}&token={self.token}")
			if response.status_code == 200:
				data = response.json()
				if data['status'] == 'OK':
					code = re.findall(r"<strong>[0-9]{6}</strong>", data["fullmessage"])
					return code[0].replace("<strong>", "").replace("</strong>", "")
				elif data['status'] == 'ERROR':
					return "WAIT_LINK"
				return KopeechkaServiceException(f'KopeechkaServiceException: Failed to receive message')
			return KopeechkaServiceException(f'KopeechkaServiceException: Kopeechka API not responding\n Status Code: {response.status_code} -> {response.text or response.content}')
		except Exception as e:
			tb = sys.exc_info()[2]
			raise KopeechkaServiceException(f'KopeechkaServiceException: get_message_email() -> {e}').with_traceback(tb)