from exceptions.exceptions import AccountNotFoundException, RoomNotFoundException
from database.pb import client

class AccountQuery:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.account_filter = f'id="{self.account_id}"'
        
    def _get_account_record(self):
        fetch = client.collection('accounts').get_list(1, 1, {'filter': self.account_filter})
        if fetch.total_items == 0:
            raise AccountNotFoundException(f"The id '{self.account_id}' does not correspond to an account.")
        return fetch.items[0]
    
    @classmethod
    def _get_account_record_by_id(cls, id: str):
        fetch = client.collection('accounts').get_list(1, 1, {'filter': f'id="{id}"'})
        if fetch.total_items == 0:
            raise  AccountNotFoundException(f"The id '{id}' does not correspond to an account.")
        return fetch.items[0]
    
    def get_display_name(self):
        return self._get_account_record().display_name
    
    def get_id(self):
        return self._get_account_record().id