from core.libraries._TrendDeliciAccount import TrendDeliciAccount
from core.libraries._TrendDeliciProduct import TrendDeliciProduct
from time import sleep
from core import DB, base

def AddFavoriteCount(count, url):
  try:
    product = TrendDeliciProduct(url)

    if product.get_product_info() == None:
      base.error("[!] Product not found")
      return

    accounts = DB.get_accounts
    base.info(f"You have {len(accounts)} accounts")

    if count > len(accounts):
      base.error("[!] You don't have enough accounts")
      base.info("[~] If you continue, it will process as much as your existing account. (Continued: C, Cancel: Q)")
      option = base.option("str", "Continue or Cancel")
      if option == "C" or option == "c":
        count = len(accounts)
      elif option == "Q" or option == "q":
        return

    base.info(f"You will add {count} favorites")

    i = 0
    for account in accounts:
      if i >= count:
        break
      base.info(f"[cyan][+][/] Email: [purple]{account['email']}[/]")
      base.info(f"[cyan][+][/] Password: [purple]************[/]")
      session = TrendDeliciAccount(account['email'], account['password'])
      if session.login:
        add_favorite = session.add_favorite(product.get_product_info())
        if add_favorite:
          base.info(f"[cyan][+][/] {url} added to favorites")
        else:
          base.info(f"[cyan][-][/] {url} not added to favorites")
      else:
        base.error("[!] Account is not active")
      base.info("\n")
      session.close()
      i += 1
  except Exception as e:
    base.error(f"[!] AddFavorite() -> {e}")
    base.error(f"[!] Product not found or error")