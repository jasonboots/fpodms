
class API:
    def __init__(self, client):
        self._client = client

    def get_all_years(self, is_north_hemisphere=None):
        if is_north_hemisphere is None:
            is_north_hemisphere = self._client.user.is_northern_hemisphere

        endpoint = 'getall'
        path = f'/api/year/{endpoint}'
        querystring = {'isNorthHemisphere': is_north_hemisphere}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def get_school_by_district(self, district_id=None, school_year_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        endpoint = 'GetByDistrict'
        path = f'/api/school/{endpoint}/{district_id}'
        querystring = {'schoolYearId': school_year_id}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def get_basclass_by_school(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        endpoint = 'GetBySchool'
        path = f'/api/class/{endpoint}/{school_id}'
        querystring = {'schoolYearId': school_year_id}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']
