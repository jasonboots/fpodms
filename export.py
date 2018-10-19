import dateutil
import re

class ExportFile:
    def __init__(self, http_response):
        self.data = self.clean_data(http_response.text)

        content_disposition_header = http_response.headers['Content-Disposition']
        filename_pattern = 'attachment; filename="(.*)"'
        filename_match = re.match(filename_pattern, content_disposition_header)
        filename = filename_match.group(1)
        self.filename = filename

        date_header = http_response.headers['Date']
        date_header_parsed = dateutil.parser.parse(date_header)
        filedate = date_header_parsed.isoformat()
        self.filedate = filedate

    @staticmethod
    def clean_data(data):
        """
        Export data has a text qualifier: ="{data}", this strips them out
        """
        regex_pattern = r'="([^\"]*)"'
        regex_replacement = r'\1'
        data_clean = re.sub(regex_pattern, regex_replacement, data)
        return data_clean

class Export:
    def __init__(self, client):
        self._client = client
        self.all_exports = [self.fpc_assessments_by_district_and_year, self.assessments_by_district_and_year, self.intervention_records_by_district_and_year]

    def export(self, endpoint, year, district_id):
        path = f'/export/{endpoint}/{district_id}'
        querystring = {'year': year}

        export_response = self._client._request('GET', path, False, params=querystring)
        return ExportFile(export_response)

    def fpc_assessments_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if year is None:
            year = self._client.preferences.year

        return self.export('FPCAssessmentsByDistrictAndYear', year, district_id)

    def assessments_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if year is None:
            year = self._client.preferences.year

        return self.export('AssessmentsByDistrictAndYear', year, district_id)

    def intervention_records_by_district_and_year(self, year=None, district_id=None):
        if district_id is None:
            district_id = self._client.preferences.district_id
        if year is None:
            year = self._client.preferences.year

        return self.export('InterventionRecordsByDistrictAndYear', year, district_id)
