from core.libraries._TrendDeliciAccount import TrendDeliciAccount
from time import sleep
from core import DB, SETTINGS, base, kopeechka, get_ip

def FollowStore(store_id):
  try:
    accounts = DB.get_accounts
    base.info(f"You have {len(accounts)} accounts")
    for account in accounts:
      base.info(f"[cyan][+][/] Email: [purple]{account['email']}[/]")
      base.info(f"[cyan][+][/] Password: [purple]************[/]")
      session = TrendDeliciAccount(account['email'], account['password'])
      if session.login:
        sleep(2)
        follow_store = session.follow_store(store_id)
        if follow_store:
          base.info(f"[cyan][+][/] {store_id} followed")
        else:
          base.info(f"[cyan][-][/] {store_id} not followed")
      else:
        base.error("[!] Account is not active")
      base.info("\n")
      session.close()
      sleep(1)
  except Exception as e:
    base.error(f"[!] FollowStore() -> {e}")
    base.error(f"[!] Store not found or error")