from . import BASE_URL, HTTP_ERROR

class Year:
    @staticmethod
    def get_all(client, is_north_hemisphere=None):
        endpoint = 'getall'
        url = f'{BASE_URL}/api/year/{endpoint}'

        if is_north_hemisphere is None:
            is_north_hemisphere = client.session_data['user']['isNorthernHemisphere']

        querystring = {'isNorthHemisphere': is_north_hemisphere}

        try:
            response = client.session.get(url, params=querystring)
            response.raise_for_status()
        except HTTP_ERROR as err:
            print(err)

        if response.ok:
            response_json = response.json()
            return response_json['data']

class School:
    @staticmethod
    def get_by_district(client, district_id=None, school_year_id=None):
        endpoint = 'GetByDistrict'

        if district_id is None:
            district_id = client.district_id

        url = f'{BASE_URL}/api/school/{endpoint}/{district_id}'

        if school_year_id is None:
            school_year_id = client.default_school_year

        querystring = {'schoolYearId': school_year_id}

        try:
            response = client.session.get(url, params=querystring)
            response.raise_for_status()
        except HTTP_ERROR as err:
            print(err)

        if response.ok:
            response_json = response.json()
            return response_json['data']

class BASClass:
    @staticmethod
    def get_by_school(client, school_id, school_year_id=None):
        endpoint = 'GetBySchool'
        url = f'{BASE_URL}/api/class/{endpoint}/{school_id}'

        if school_year_id is None:
            school_year_id = client.default_school_year

        querystring = {'schoolYearId': school_year_id}

        try:
            response = client.session.get(url, params=querystring)
            response.raise_for_status()
        except HTTP_ERROR as err:
            print(err)

        if response.ok:
            response_json = response.json()
            return response_json['data']