from core.libraries._TrendDeliciAccount import TrendDeliciAccount
from core.libraries._TrendDeliciProduct import TrendDeliciProduct
from time import sleep
from core import DB, base

def AddFavorite(url):
  try:
    product = TrendDeliciProduct(url)

    if product.get_product_info() == None:
      base.error("[!] Product not found")
      return

    accounts = DB.get_accounts
    base.info(f"You have {len(accounts)} accounts")

    for account in accounts:
      base.info(f"[cyan][+][/] Email: [purple]{account['email']}[/]")
      base.info(f"[cyan][+][/] Password: [purple]************[/]")
      session = TrendDeliciAccount(account['email'], account['password'])
      if session.login:
        sleep(2)
        add_favorite = session.add_favorite(product.get_product_info())
        if add_favorite:
          base.info(f"[cyan][+][/] {url} added to favorites")
        else:
          base.info(f"[cyan][-][/] {url} not added to favorites")
      else:
        base.error("[!] Account is not active")
      base.info("\n")
      session.close()
      sleep(3)
  except Exception as e:
    base.error(f"[!] AddFavorite() -> {e}")
    base.error(f"[!] Product not found or error")