import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from automatisation.scramble import TimeEditScramble
import re

class TimeEditAPI:
    # Global variables
    auth_url = "https://cloud.timeedit.net/chalmers/web/timeedit/sso/saml2"
    session : requests.Session
    CID_USERNAME : str
    CID_PASSWORD : str
    hasLoggedin : bool = False
    faildCount : int = 0
    scramble = TimeEditScramble()
    
    def __init__(self, CID_USERNAME: str = None, CID_PASSWORD: str = None, cookies: dict = None):
        if (cookies is not None):
            self.session = requests.Session()
            self.session.cookies.update(cookies)
            return
        else:
            # Set CID_USERNAME and CID_PASSWORD
            if (CID_USERNAME is not None and CID_PASSWORD is not None):
                self.CID_USERNAME = CID_USERNAME
                self.CID_PASSWORD = CID_PASSWORD
            else:
                load_dotenv()
                self.CID_USERNAME = os.getenv("CID_USERNAME")
                self.CID_PASSWORD = os.getenv("CID_PASSWORD")
            if (self.CID_USERNAME is None or self.CID_PASSWORD is None):
                raise Exception("CID_USERNAME or CID_PASSWORD not found in .env file")
            # Create new session
            self.session = requests.Session()
            # try to login
            self.login()
   
    @staticmethod
    def get_instance_from_cookies(cookies: dict):
        instance = TimeEditAPI(cookies=cookies)
        if not instance.test():
            raise Exception("Invalid cookies")
        return instance
        
    def is_session_valid(self):
        return self.test()
    
    def test(self):
        try:
            response = self.session.get("https://cloud.timeedit.net/chalmers/web/b1/ri1Q5008.html")
            if (response.status_code == 200):
                self.hasLoggedin = True
                return True
            self.hasLoggedin = False
            return False
        except requests.exceptions.RequestException as e:
            raise Exception("Failed to validate session: " + str(e))
        
    def get_cookies(self):
        return self.session.cookies.get_dict()
        
    def login(self):
        response = self.session.get(self.auth_url)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form")
        action = form["action"]
        form_url = f"https://idp.chalmers.se{action}"  
        data = {
            'UserName':  self.CID_USERNAME,  
            'Password':  self.CID_PASSWORD,
            'AuthMethod': 'FormsAuthentication'
        }
        error = None
        response = self.session.post(form_url, data=data)
        soup_form = BeautifulSoup(response.text, "html.parser")
        form = soup_form.find("span", id="errorText")
        if form:
            print(form.text)
            error_message = form.text
            if error_message:
                error = error_message
        if error:
            error = "❌ Login failed, " + error
            raise Exception(error)
        else:
            print( "🔗 Redirecting to TimeEdit")
            
        form_response_soup  = BeautifulSoup(response.text, "html.parser")
        form = form_response_soup.find('form')
        action_url = form['action']
        data = {input_tag['name']: input_tag['value'] for input_tag in form.find_all('input', type='hidden')}
        response = self.session.post(action_url, data=data)

        if response.ok:
            print( "✅ Login successful with CID")
            self.hasLoggedin = True
        else:
            raise Exception("❌ Login failed with CID")

    # pass the args to as_url
    def get_reservations(self, from_date: datetime = None, to_date: datetime = None) -> dict:
        reservations_url = self.scramble.as_url( from_date=from_date, to_date=to_date)
        response = self.session.get(reservations_url)
        try:
            response_json = response.json()
            return response_json
        except:
            if (self.faildCount > 3):
                raise Exception("Failed to get reservations, might be a problem with the TimeEdit API")
            else:
                # Attempt to login again
                print("Failed to get reservations, attempting to login again")
                self.login()
                self.faildCount += 1 
                self.get_reservations()
    def gen_csttg(self):
        response = self.session.post('https://cloud.timeedit.net/chalmers/web/b1/ri1Q5008.html', data={ 'CSTTG': 'gen' })
        return response.text            
    
    def reserve_grouproom(self, grouproom_id: str, date:str, starttime:str, endtime:str):
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date format is incorrect")
        if not re.match(r'^\d{2}:\d{2}$', starttime) or not re.match(r'^\d{2}:\d{2}$', endtime):
            raise ValueError("Time format is incorrect")

        data = {
            'kind': 'reserve',
            'nocache': '4',
            'l': 'sv_SE',
            'o': [f'{grouproom_id}.186', '203460.192'],
            'aos': '',
            'dates': str(date),
            'starttime':  str(starttime),
            'endtime': str(endtime),
            'url': 'https://cloud.timeedit.net/chalmers/web/b1/ri1Q5008.html',
            'fe2': '',
            'fe8': '',
            'CSTT': str(self.gen_csttg())
        }
        response = self.session.post('https://cloud.timeedit.net/chalmers/web/b1/ri1Q5008.html', data=data)
        if (response.status_code != 200):
            raise Exception("Status: " + str(response.status_code) + " | " + response.text)

        print(f"🎉 Room reserved | id: {grouproom_id} date:{date} {starttime}-{endtime}")
        return response
        
    def get_all_my_reservations(self):
        response = self.session.get("https://cloud.timeedit.net/chalmers/web/b1/my.json")
        if response.status_code == 200:
            response_json  = response.json()
            if (response_json['reservations'] is not None or response_json['reservationcount'] > 0):
                reservations = response_json['reservations']
                return reservations
            return []
        
        raise Exception("Failed to get reservations")
    
    def delete_reservation(self, reservation_id: str):
        params = {
            'id': str(reservation_id),
            'l': 'sv_SE',
            'sid': '1005',
        }
        response = self.session.delete('https://cloud.timeedit.net/chalmers/web/b1/my.html', params=params)
        if response.status_code == 200:
            print(f"Reservation deleted | id: {reservation_id}")
            return response
    
        raise Exception("Failed to delete reservation")

    def edit_reservation(self, reservation_id: str, date:str, starttime:str, endtime:str):
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date format is incorrect")
        if not re.match(r'^\d{2}:\d{2}$', starttime) or not re.match(r'^\d{2}:\d{2}$', endtime):
            raise ValueError("Time format is incorrect")
        #convert date to correct format
        starttime = starttime.replace(":", ".")
        endtime = endtime.replace(":", ".")
        params = {
            'h': 't',
            'sid': '1005',
            'id': str(reservation_id),
            'fr': 't',
            'step': '3',
            'myp': 't',
            'ef': '2',
            'nocache': '2',
        }
        data = {
            'ef': '3',
            't': f'{starttime},{endtime}',
            'dates': f'{date}-undefined',
            'CSTT': str(self.gen_csttg())
        }
        response = self.session.post('https://cloud.timeedit.net/chalmers/web/b1/my.html', params=params, data=data)
        if response.status_code == 200:
            print(f"Reservation edited | id:{reservation_id}")
            return response
        error_message = response.text
        if(error_message and len(error_message) > 0 and len(error_message) < 100):
            raise Exception(error_message)
        raise Exception("Failed to edit reservation")
        
if __name__ == "__main__":
    timeedit = TimeEditAPI()
    # timeedit.reserve_grouproom("192564", "20240503", "08:00", "10:00")
    print(timeedit.get_all_my_reservations())
    # timeedit.edit_reservation("2067402", "20240503", "08:00", "10:00")
    
    