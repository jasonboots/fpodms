import requests

BASE_URL = 'https://fpdms.heinemann.com'
HTTP_ERROR = requests.exceptions.HTTPError

class Client:
    """An F&P ODMS session.

    :param email_address: A string, a valid login email address.
    :param password: A string, a valid login email address.
    """
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

        login_url = f'{BASE_URL}/api/account/login'
        session_payload = {'emailAddress': email_address, 'password': password}
        try:
            session = requests.session()
            login_response = session.post(login_url, data=session_payload)
            login_response.raise_for_status()
        except HTTP_ERROR as err:
            print(err)

        if login_response.ok:
            login_response_json = login_response.json()

            self.session = session
            self.session_data = login_response_json['data']
            self.district_id = login_response_json['data']['preferences']['districtId']
            self.default_school_year = login_response_json['data']['preferences']['schoolYear']

__all__ = ['api', 'export']
import fpodms.api
import fpodms.export