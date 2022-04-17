from core import SETTINGS, base, DB, kopeechka
from core.options import FollowStore, AddFavorite, GetCoupons, ShowAccounts, CreateAccounts, AddFavoriteCount
from time import sleep

def main():
    balance = kopeechka.get_balance()

    if balance == 0:
        base.error("[!] Your balance is 0")
        return
    if balance == None:
        base.error("[!] Kopeechka API is not responding")
        return
    
    base.info(f"[blue]Kopeechka : [/][purple]{balance} RUB [/][blue](estimated {int(balance / 0.2)} mail)[/] | [blue]Proxy : [/][purple]{SETTINGS['proxy']}[/] | [blue]Account Password : [/][purple]{SETTINGS['default_password']}[/]", False)
    
    base.console.print("""
    [green][[/][yellow] 0 [/][green]][/] [cyan]Create Account[/]
    [green][[/][yellow] 1 [/][green]][/] [cyan]Show Accounts[/]
    [green][[/][yellow] 2 [/][green]][/] [cyan]Get Coupons[/]

    [green][[/][yellow] 3 [/][green]][/] [cyan]Add Favorite[/]
    [green][[/][yellow] 4 [/][green]][/] [cyan]Adding a certain number of favorites[/]


    [green][[/][yellow] 5 [/][green]][/] [cyan]Follow Store[/]
    [green][[/][yellow] q [/][green]][/] [cyan]Quit[/]
    """)
    option = base.option("str", "Choose the option you want to do")

    if option == '0':
        base.clear
        base.logo_print()
        base.detail_print()

        balance = kopeechka.get_balance()

        base.info(f"[blue]Kopeechka : [/][purple]{balance} RUB [/][blue](estimated {int(balance / 0.2)} mail)[/] | [blue]Proxy : [/][purple]{SETTINGS['proxy']}[/] | [blue]Account Password : [/][purple]{SETTINGS['default_password']}[/]\n", False)
    
        count = base.option("int", "How many accounts do you want to create?")
        mail = base.option("str", "Which email do you need? empty: mail.ru")
        if mail == "":
            mail = "mail.ru"
        CreateAccounts(count, mail)
    elif option == '1':
        base.clear
        base.logo_print()
        base.detail_print()
        
        ShowAccounts()
    elif option == '2':
        base.clear
        base.logo_print()
        base.detail_print()

        GetCoupons()
    elif option == '3':
        base.clear
        base.logo_print()
        base.detail_print()

        url = base.option("str", "The product link you want to add to favourite")
        AddFavorite(url)
    elif option == '4':
        base.clear
        base.logo_print()
        base.detail_print()

        count = base.option("int", "How many Favorites do you want to add?")
        url = base.option("str", "The product link you want to add to favourite")
        AddFavoriteCount(count, url)
    elif option == '5':
        base.clear
        base.logo_print()
        base.detail_print()

        store_id = base.option("str", "Enter the store ID you want to track")
        FollowStore(store_id)
    else:
        base.clear
        base.console.print("[red]Program terminated[/]")
        sleep(.5)
        exit()

if __name__ == '__main__':
    main()