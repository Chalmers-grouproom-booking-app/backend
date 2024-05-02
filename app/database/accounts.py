from database.pb import client
from utils import decrypt_data, encrypt_data
import json
import random
from exceptions.exceptions import InvalidDataError, AccountCreationError, AccountNotFoundError

def generate_random_display_name():
    return "Anonymous" + str(random.randint(1000, 9999)) + ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))

def encrypt_json(json_data):
    try:
        return encrypt_data(json.dumps(json_data))
    except json.JSONDecodeError:
        raise InvalidDataError("Provided cookies are not valid JSON")

def decrypt_json(encrypted_data):
    try:
        return json.loads(decrypt_data(encrypted_data))
    except json.JSONDecodeError:
        raise InvalidDataError("Provided cookies are not valid JSON")

class AccountPB:
    collection = client.collection('accounts')
    
    def __init__(self, account_obj):
            self.id = account_obj.id
            self.token = account_obj.token
            self.email = account_obj.email
            self.display_name = account_obj.display_name
            self.cookies = account_obj.cookies  # No need to decrypt here
        
    def timeedit_cookies(self):
        try:
            return decrypt_json(self.cookies) if self.cookies is not None else {}
        except InvalidDataError:
            return {}
        
    @staticmethod
    def query_one(filter, limit=1, offset=1):
        try:
            result = AccountPB.collection.get_list(limit, offset, {'filter': filter})
            if result.total_items == 0:
                raise AccountNotFoundError("Account not found")
            return AccountPB(result.items[0])
        except Exception as e:
            raise AccountNotFoundError(f"Failed to fetch account: {str(e)}")

    @staticmethod   
    def get_account(token: str):
        account_obj = AccountPB.query_one(f'token="{token}"')
        if account_obj is None:
            raise AccountNotFoundError("Account not found")
        return AccountPB(account_obj)

    @staticmethod
    def get_account_by_email(email: str):
        account_obj = AccountPB.query_one(f'email="{email}"')
        if account_obj is None:
            raise AccountNotFoundError("Account not found")
        return AccountPB(account_obj)
    
    @staticmethod
    def create_account(token, email, display_name=None, cookies=None):
        try:
            cookies_encrypted = encrypt_json(cookies) if cookies is not None else None
            account_obj = AccountPB.collection.create({
                'token': token,
                'email': email,
                'display_name': display_name or generate_random_display_name(),
                'cookies': cookies_encrypted
            })
            return AccountPB(account_obj)
        except Exception as e:
            raise AccountCreationError(f"Failed to create account: {str(e)}")

    #static method boolean if display name is unique
    @staticmethod
    def is_display_name_unique(display_name):
        result = AccountPB.collection.get_list(1, 1, {'filter': f'display_name="{display_name}"'})
        return result.total_items == 0

    def update_account(self, display_name=None, cookies=None):
        updates = {}
        if display_name is not None:
            self.display_name = display_name
            updates['display_name'] = display_name
        if cookies is not None:
            encrypted_cookies = encrypt_json(cookies)
            self.cookies = cookies  # store decrypted cookies internally
            updates['cookies'] = encrypted_cookies

        if updates:
            AccountPB.collection.update(self.id, updates)
        return self