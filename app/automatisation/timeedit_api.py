import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from automatisation.scramble import TimeEditScramble

class TimeEditAPI:
    # Global variables
    auth_url = "https://cloud.timeedit.net/chalmers/web/timeedit/sso/saml2"
    session : requests.Session
    CID_USERNAME : str
    CID_PASSWORD : str
    hasLoggedin : bool = False
    faildCount : int = 0
    scramble = TimeEditScramble()
    def __init__(self, auth_url = None):
        if (auth_url is not None):
            self.auth_url = auth_url
        load_dotenv()
        # Set CID_USERNAME and CID_PASSWORD
        self.CID_USERNAME = os.getenv("CID_USERNAME")
        self.CID_PASSWORD = os.getenv("CID_PASSWORD")
        if (self.CID_USERNAME is None or self.CID_PASSWORD is None):
            raise Exception("CID_USERNAME or CID_PASSWORD not found in .env file")
        # Create new session
        self.session = requests.Session()
        # Attempt to authenticate with CID
        self.login()

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
            error = "❌ Login failed with CID, " + error
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

if __name__ == "__main__":
    timeedit = TimeEditAPI()
    print(timeedit.get_reservations(  from_date=datetime.now(), to_date=datetime.now() + timedelta(days=7)))