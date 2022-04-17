from core.libraries._TrendDeliciAccount import TrendDeliciAccount
from time import sleep
from core import DB, base

def GetCoupons():
  try:
    accounts = DB.get_accounts
    base.info(f"You have {len(accounts)} accounts")
    for account in accounts:
      base.info(f"[cyan][+][/] Email: [purple]{account['email']}[/]")
      base.info(f"[cyan][+][/] Password: [purple]************[/]")
      session = TrendDeliciAccount(account['email'], account['password'])
      if session.login:
        sleep(2)
        coupons = session.get_coupons()
        if coupons:
          base.info(f"[cyan][+][/] {len(coupons)} coupons found")
        else:
          base.info("[cyan][-][/] No coupons")
      else:
        base.error("[!] Account is not active")
      base.info("\n")
      session.close()
      sleep(1)
  except Exception as e:
    base.error(f"[!] GetCoupons() -> {e}")
    base.error(f"[!] an unknown error")