import requests
from base.FribeBase import FribeBase
from core.libraries._TinyDB import AccountsDB
from core.libraries._KopeechkaService import KopeechkaService

base = FribeBase(
    "TrendDelici",
    tab=3
)

DB = AccountsDB()

SETTINGS = base.json_load("settings.json")

if SETTINGS:
    base.info("Settings loaded")
else:
    base.error("Settings not found -> base settings loaded")
    SETTINGS = {}

if "default_password" not in SETTINGS:
    SETTINGS['default_password'] = "12345678aA"

if "kopeechka" not in SETTINGS:
    SETTINGS['kopeechka'] = "YOUR_KOPEECHKA_API_KEY"

if "proxy" not in SETTINGS:
    SETTINGS['proxy'] = False

if "proxies" not in SETTINGS:
    SETTINGS['proxies'] = [""]

kopeechka = KopeechkaService(SETTINGS['kopeechka'])

def get_ip():
    try:
        if SETTINGS["proxy"]:
            return SETTINGS["proxies"][0].split("@")[-1].split(":")[0]
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        return None