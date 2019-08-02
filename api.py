#!/bin/python3.6
class API:
    def __init__(self, client):
        self._client = client

    def all_years(self, is_north_hemisphere=None):
        if is_north_hemisphere is None:
            is_north_hemisphere = self._client.user.is_northern_hemisphere

        endpoint = 'getall'
        path = f'/api/year/{endpoint}'
        querystring = {'isNorthHemisphere': is_north_hemisphere}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def school_by_district(self, district_id=None, school_year_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        endpoint = 'GetByDistrict'
        path = f'/api/school/{endpoint}/{district_id}'
        querystring = {'schoolYearId': school_year_id}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def basclass_by_school(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        endpoint = 'GetBySchool'
        path = f'/api/class/{endpoint}/{school_id}'
        querystring = {'schoolYearId': school_year_id}

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def students_by_school_and_school_year(self, school_id, school_year_id=None):
        if school_year_id is None:
            school_year_id = self._client.preferences.year

        endpoint = 'GetStudentsBySchoolAndSchoolYear'
        path = f'/api/school/{endpoint}'
        querystring = {
            'schoolId': school_id,
            'schoolYear': school_year_id,
        }

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def grade_by_school(self, school_id, in_use_only=True):
        endpoint = 'GetBySchool'
        path = f'/api/grade/{endpoint}/{school_id}'
        querystring = {
            'inUseOnly': in_use_only,
        }

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']

    def add_student(self, **kwargs):
        endpoint = 'AddStudent'
        path = f'/api/student/{endpoint}'
        payload = {
            'student': {
                'firstName': kwargs['firstName'],
                'lastName': kwargs['lastName'],
                'studentIdentifier': kwargs['studentIdentifier'],
            },
            'studentSchoolYear': {
                'schoolYearId': kwargs['schoolYearId'],
                'schoolId': kwargs['schoolId'],
                'gradeId': kwargs['gradeId'],
            },
            'classStudent': {
                'classId': '',
                'fpcclassId': '',
                'groupId': '',
            },
        }

        response = self._client._request('POST', path, True, data=payload)
        return response['data']

    def add_student_to_school_and_grade_and_maybe_class(self, **kwargs):
        endpoint = 'AddStudentToSchoolAndGradeAndMaybeClass'
        path = f'/api/student/{endpoint}'
        payload = {
            'studentId': kwargs['studentId'],
            'schoolYearId': kwargs['schoolYearId'],
            'schoolId': kwargs['schoolId'],
            'gradeId': kwargs['gradeId'],
            'classStudentStartDate': kwargs['classStudentStartDate'],
            'classStudentEndDate': kwargs['classStudentEndDate'],
            'active': True,
            'classId': None,
            'className': None,
            'classStartDate': None,
            'classEndDate': None,
            'schoolLunchProgram': False,
            'specialEducationServices': False,
            'additionalReadingServices': False,
            'otherServicesPrograms': False,
            'otherServicesDescription': '',
            'calendar': {
                'sortComprehension': {},
                'loadingHelper': {},
                'isReady': True,
                'start': {},
                'end': {},
                'holidays': [],
            },
        }

        response = self._client._request('POST', path, True, data=payload)
        return response

    def student_school_years_and_classes(self, student_id):
        endpoint = 'GetStudentSchoolYearsAndClasses'
        path = f'/api/student/{endpoint}'
        querystring = {
            'studentId': student_id,
        }

        response = self._client._request('GET', path, True, params=querystring)
        return response['data']