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
    except (json.JSONDecodeError, TypeError) as e:
        raise InvalidDataError(f"Provided data are not valid JSON: {str(e)}")

def decrypt_json(encrypted_data):
    try:
        return json.loads(decrypt_data(encrypted_data))
    except (json.JSONDecodeError, TypeError) as e:
        raise InvalidDataError(f"Decryption failed or resulted in invalid JSON: {str(e)}")

class AccountPB:
    collection = client.collection('accounts')
    
    def __init__(self, account_obj):
        self.id = account_obj.id
        self.token = account_obj.token
        self.email = account_obj.email
        self.display_name = account_obj.display_name
        self.cookies = account_obj.cookies 

    def timeedit_cookies(self):
        return decrypt_json(self.cookies) if self.cookies else {}

    @staticmethod
    def query_one(filter):
        try:
            result = AccountPB.collection.get_list(1, 1, {'filter': filter})
            if result.total_items == 0:
                raise AccountNotFoundError("Account not found")
            return AccountPB( result.items[0] )
        except Exception as e:
            raise AccountNotFoundError(f"Failed to fetch account: {str(e)}")

    @classmethod
    def get_account(cls, token: str):
        return cls.query_one(f'token="{token}"')

    @classmethod
    def get_account_by_email(cls, email: str):
        return cls.query_one(f'email="{email}"')
    
    @classmethod
    def create_account(cls, token, email, display_name=None, cookies=None):
        try:
            cookies_encrypted = encrypt_json(cookies) if cookies else None
            # Assuming `create` method returns the created object.
            account_obj = AccountPB.collection.create({
                'token': token,
                'email': email,
                'display_name': display_name or generate_random_display_name(),
                'cookies': cookies_encrypted
            })
            return cls(account_obj)
        except Exception as e:
            raise AccountCreationError(f"Failed to create account: {str(e)}")

    @classmethod
    def is_display_name_unique( cls, display_name):
        count = cls.collection.get_list(1, 1, {'filter': f'display_name="{display_name}"'}).total_items
        return count == 0

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
        
    @classmethod
    def get_or_create_account(cls, token, email, **kwargs):
        try:
            account = cls.get_account(token)
        except AccountNotFoundError:
            account = cls.create_account(token, email, **kwargs)
        return account