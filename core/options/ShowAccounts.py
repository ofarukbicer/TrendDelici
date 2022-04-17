from core.libraries._TrendDeliciAccount import TrendDeliciAccount
from time import sleep
from core import DB, base

def ShowAccounts():
  try:
    accounts = DB.get_accounts
    base.info(f"You have {len(accounts)} accounts")
    for account in accounts:
      base.info(f"[cyan][+][/] Email: [purple]{account['email']}[/]")
      base.info(f"[cyan][+][/] Password: [purple]{account['password']}[/]")
      session = TrendDeliciAccount(account['email'], account['password'])
      if session.login:
        base.info("[cyan][+][/] Account is active")
      else:
        base.error("[cyan][-][/] Account is not active")
        del_ac = base.option("str", "Delete this account? (Y/N)")
        if del_ac == "Y" or del_ac == "y":
          DB.delete(account['email'])
          base.info("[cyan][+][/] Account deleted")
          base.info("\n")
      base.info("\n")
      session.close()
      sleep(3)
  except Exception as e:
    base.error(f"[!] ShowAccounts() -> {e}")
    base.error(f"[!] an unknown error")