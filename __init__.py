import requests
import inflection

BASE_URL = 'https://fpdms.heinemann.com'
HTTP_ERROR = requests.exceptions.HTTPError

class Client:
    """An F&P ODMS session.

    :param email_address: A string, a valid login email address.
    :param password: A string, a valid login email address.
    """
    def __init__(self, email_address, password):
        login_url = f'{BASE_URL}/api/account/login'
        session_payload = {'emailAddress': email_address, 'password': password}
        try:
            session = requests.session()
            login_response = session.post(login_url, data=session_payload)
            login_response.raise_for_status()
        except HTTP_ERROR as err:
            print(err)

        if login_response.ok:
            self.session = session

            login_response_json = login_response.json()
            session_data = _SessionData(**login_response_json['data'])

            self.preferences = session_data.preferences
            self.session_timeout_minutes = session_data.session_timeout_minutes
            self.state = session_data.state
            self.user = session_data.user

class _SessionData:
    def __init__(self, **session_data):
        for k, v in session_data.items():
            k = k.replace('.', '_')
            k = inflection.camelize(k)
            k = inflection.underscore(k)

            if isinstance(v, dict):
                self.__dict__[k] = _SessionData(**v)
            else:
                self.__dict__[k] = v

__all__ = ['api', 'export']
import fpodms.api
import fpodms.export