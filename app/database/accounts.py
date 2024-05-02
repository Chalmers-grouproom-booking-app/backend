from database.pb import client
from utils import decrypt_data, encrypt_data
import json
import random

def generate_random_display_name():
    return "Anonymous" + str(random.randint(1000, 9999)) + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))

class AccountPB:
    collection = client.collection('accounts')
    
    def __init__(self, account_obj):
        self.id = account_obj.id
        self.token = account_obj.token
        self.email = account_obj.email
        self.display_name = account_obj.display_name
        if (account_obj.cookies != None):
            self.timeedit_cookies = json.loads( decrypt_data(account_obj.cookies) )
    
    @staticmethod
    def query_one( filter, limit = 1, offset = 1):
        try:
            result  = AccountPB.collection.get_list(limit, offset, {'filter': filter})
            if (result.total_items != 0):
                return AccountPB(result.items[0])
            return None
        except:
            return None
    
    @staticmethod   
    def get_account(token: str):
        account_obj = AccountPB.query_one(f'token="{token}"')
        if (account_obj == None):
            raise Exception("Account not found")
        return AccountPB(account_obj)

    @staticmethod
    def get_account_by_email(email: str):
        account_obj = AccountPB.query_one(f'email="{email}"')
        if (account_obj == None):
            raise Exception("Account not found")
        return AccountPB(account_obj)
    
    @staticmethod
    def create_account( token: str, email: str, display_name: str = None, cookies: str = None):
        try:
            cookies_encrypted = None
            if cookies != None:
                cookies_encrypted = encrypt_data( json.dumps(cookies) )
            account_obj = AccountPB.collection.create({
                'token': token,
                'email': email,
                'display_name': display_name if display_name != None else generate_random_display_name(),
                'cookies': cookies_encrypted
            })
            return AccountPB(account_obj)
        except json.JSONDecodeError:
            raise Exception("Invalid cookies")
        except:
            raise Exception("Account already exists")
        

    def update(self, display_name: str = None, cookies: str = None):
        encrypt_cookies = None
        if (display_name != None):
            self.display_name = display_name
        if (cookies != None):
            encrypt_cookies = encrypt_data( json.dumps(cookies) )
            self.timeedit_cookies = cookies
        AccountPB.collection.update(self.id, {
            'display_name': self.display_name,
            'timeedit_cookies':  encrypt_cookies
        })
        return self


if __name__ == "__main__":
    account  = AccountPB.get_account("1234")
    account2 = AccountPB.create_account("3123", "emai@dmao")