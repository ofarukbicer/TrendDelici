from tinydb import TinyDB, Query
from tinydb.operations import delete
from tinydb.queries import QueryLike

class AccountsDB:
    def __init__(self):
        TinyDB.default_table_name = self.__class__.__name__
        self.db    = TinyDB(f"@Accounts_DB.json", ensure_ascii=False, indent=2, sort_keys=False)
        self.sorgu = Query()

    def search(self, sorgu:QueryLike):
        arama = self.db.search(sorgu)
        say   = len(arama)
        if say == 1:
            return arama[0]
        elif say > 1:
            cursor = arama
            return [
                {
                    "email": bak["email"],
                    "password": bak["password"],
                    "createdIp": bak["createdIp"],
                }
                for bak in cursor
            ]
        else:
            return None

    def add(self, email, password, createdIp):
        if not self.search(self.sorgu.email == email):
            return self.db.insert({
                "email": email,
                "password": password,
                "createdIp": createdIp,
            })
        else:
            return None

    def delete(self, email):
        if not self.search(self.sorgu.email == email):
            return None

        # self.db.update(delete('uye_id'), self.sorgu.uye_id == uye_id)
        self.db.remove(self.sorgu.email == email)
        return True

    @property
    def get_accounts(self):
        return self.search(self.sorgu.email.exists())