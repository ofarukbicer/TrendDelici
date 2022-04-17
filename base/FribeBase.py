# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır değişikler @ofarukbicer tarafından yapılmıştır.

from pyfiglet import Figlet
import os, platform, requests, datetime, pytz
from rich.console import Console
from requests.exceptions import ConnectionError
from json import dumps, loads

class FribeBase():
    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- fribe.org projelerinde kullanmak üzere tasarlanmıştır."

    console:Console = Console(log_path=False, highlight=False)

    try:
        username = os.getlogin()
    except OSError:
        import pwd
        username = pwd.getpwuid(os.geteuid())[0]

    pc_name = platform.node()
    session = username + "@" + pc_name

    operating_system = platform.system()
    firmware_version = platform.release()
    device = operating_system + " | " + firmware_version

    date = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%d-%m-%Y")
    hour  = datetime.datetime.now(pytz.timezone("Turkey")).strftime("%H:%M")
    time = date + " | " + hour

    try:
        global_ip = requests.get('http://ip-api.com/json').json()['query']
    except ConnectionError:
        global_ip = requests.get('https://api.ipify.org').text
    except Exception as hata:
        global_ip = type(hata).__name__

    top_detail = f"[bright_red]{device}[/]\t\t[bright_yellow]{time}[/]\n\n"
    top_detail += f"[turquoise2]{session}[/]\n"
    top_detail += f"[yellow2]{global_ip}[/]\n"

    def get_location(self):
        location = os.getcwd()
        return location.split("\\") if self.operating_system == "Windows" else location.split("/")

    def __init__(self, banner:str, width:int=70, tab:int=0, style:str="stop") -> None:
        self.width = width
        self.logo = Figlet(font=style).renderText(f"{' ' * tab}{banner}")

        self.clear
        self.console.print(self.logo, width=width, style="green")
        self.console.print(self.top_detail, width=width, justify="center")

    def logo_print(self, color:str="turquoise2") -> None:
        self.clear
        self.console.print(self.logo, width=self.width, justify="center", style=color)

    def detail_print(self):
        self.console.print(self.top_detail, width=self.width, justify="center")

    def info_log(self, left:str, center:str, right:str) -> None:
        left  = f"{left[:25]}[bright_blue]~[/]"   if len(left)  > 26 else left
        center = f"{center[:21]}[bright_blue]~[/]"  if len(center) > 22 else center
        right  = f"{right[:14]}[bright_blue]~[/]"   if len(right)  > 15 else right
        format = '[bold red]{:14}[/] [green]||[/] [yellow]{:20}[/] {:>2}[green]||[/] [magenta]{:^16}[/]'.format(left, center, "", right)
        self.console.log(format)

    def info(self, text:str, clock:bool = True) -> None:
        format = f'[bold green]{text}[/]'
        if clock:
            self.console.log(format)
        else:
            self.console.print(format)

    def error(self, text:str) -> None:
        format = f'[bold red]{text}[/]'
        self.console.log(format)

    def error_log(self, hata:Exception) -> None:
        format = f'\t  [bold yellow2]{type(hata).__name__}[/] [bold magenta]||[/] [bold grey74]{hata}[/]'

        self.console.print(f"{format}", width=self.width, justify="center")

    def json_print(self, json_data:dict, color:str="turquoise2") -> None:
        self.console.print(dumps(json_data, indent=2, ensure_ascii=False, sort_keys=True), justify="left", style=color)

    def json_save(self, json_data:dict, file_name:str) -> None:
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(dumps(json_data, indent=2, ensure_ascii=False, sort_keys=True))
            file.close()

    def json_load(self, file_name:str) -> None:
        if not os.path.exists(file_name):
            f = open(file_name, "w")
            f.write("")
            f.close()
        with open(file_name, "r", encoding='utf-8') as file:
            veri = file.read()
            if veri == "":
                file.close()
                return None
            data = loads(veri)
            file.close()
        return data

    def option(self, type:str = "str", info:str = ""):
        if type == "str" or type == "string":
            return str(self.console.input(f"[red]{self.session}:[/][cyan]~/../{self.get_location()[-2] + '/' + self.get_location()[-1]}[/]{' [green][[/][yellow] ' + info + ' [/][green]][/] ' if info else ''}[cyan]>> "))
        elif type == "int" or type == "integer":
            return int(self.console.input(f"[red]{self.session}:[/][cyan]~/../{self.get_location()[-2] + '/' + self.get_location()[-1]}[/]{' [green][[/][yellow] ' + info + ' [/][green]][/] ' if info else ''}[cyan]>> "))
        else:
            return str(self.console.input(f"[red]{self.session}:[/][cyan]~/../{self.get_location()[-2] + '/' + self.get_location()[-1]}[/]{' [green][[/][yellow] ' + info + ' [/][green]][/] ' if info else ''}[cyan]>> "))

    @property
    def clear(self) -> None:
        if self.operating_system == "Windows":
            os.system("cls")
        else:
            os.system("clear")