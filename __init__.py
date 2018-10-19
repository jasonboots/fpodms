#!/python3.6
import requests
import inflection

HTTP_ERROR = requests.exceptions.HTTPError

class Client:
    """An F&P ODMS session.

    :param email_address: A string, a valid login email address.
    :param password: A string, a valid login email address.
    """
    def __init__(self, email_address, password):
        self.base_url = 'https://fpdms.heinemann.com'
        self.session = requests.session()

        login_path = '/api/account/login'
        login_payload = {'emailAddress': email_address, 'password': password}
        login_response = self._request('POST', login_path, True, data=login_payload)

        session_data = _SessionData(**login_response['data'])
        self.preferences = session_data.preferences
        self.session_timeout_minutes = session_data.session_timeout_minutes
        self.state = session_data.state
        self.user = session_data.user

        self.api = api.API(self)
        self.export = export.Export(self)

    def _request(self, method, path, json_response, params=None, data=None):
        url = f'{self.base_url}{path}'
        try:
            response = self.session.request(method, url, params=params, data=data)
            response.raise_for_status()

            if json_response:
                return response.json()
            else:
                return response

        except HTTP_ERROR as e:
            print(e)

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

from fpodms import api
from fpodms import export
