from core.libraries._TrendDeliciAuth import TrendDeliciAuth
from time import sleep
from core import DB, SETTINGS, base, kopeechka, get_ip

def CreateAccounts(count = 1, mail = "mail.ru"):
  try:
    trend_delici = TrendDeliciAuth()

    base.info(f"{count} accounts are created")
    
    for i in range(count):
      random_mail = kopeechka.get_email("trendyol.com", mail)
      base.info(f"[cyan][+][/] Email: [purple]{random_mail['mail']}[/]")
      base.info(f"[cyan][+][/] ID: [purple]{random_mail['id']}[/]")

      validate = trend_delici.validate_email(random_mail['mail'])
      
      if validate:
          signup = trend_delici.signup(random_mail['mail'], SETTINGS['default_password'])
          code = ""
          sleep(10)
          if signup.status:
              while True:
                  code = kopeechka.get_verification_code(random_mail['id'])
                  if code == "WAIT_LINK":
                      sleep(5)
                  else:
                      base.info(f"[cyan][+][/] Verification Code: {code}")
                      break
              if code:
                  account_verification = signup.account_verification(code)
                  if "accessToken" in account_verification:
                      base.info(f"[cyan][+][/] Signup Successful")
                      DB.add(
                          random_mail['mail'],
                          SETTINGS['default_password'],
                          get_ip() or "ip not found",
                      )
                  else:
                      base.error(f"[-] Verification Failed")
              else:
                  base.error(f"[-] Verification Code not received")
          else:
              base.error("[!] Signup Failed")
      else:
          base.error("[!] Email is not valid")
      base.info(f"{i+1}/{count} accounts are created")
  except Exception as e:
    base.error(f"[!] CreateAccounts() -> {e}")
    base.error(f"[!] an unknown error")