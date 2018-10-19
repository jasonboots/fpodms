from . import BASE_URL, HTTP_ERROR
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

def export(client, endpoint, year, district_id):
    export_url = f'{BASE_URL}/export/{endpoint}/{district_id}'
    querystring = {'year': year}

    try:
        export_response = client.session.get(export_url, params=querystring)
        export_response.raise_for_status()
    except HTTP_ERROR as err:
        print(err)

    if export_response.ok:
        return ExportFile(export_response)

def fpc_assessments_by_district_and_year(client, year=None, district_id=None):
    if district_id is None:
        district_id = client.preferences.district_id
    if year is None:
        year = client.preferences.year

    return export(client, 'FPCAssessmentsByDistrictAndYear', year, district_id)

def assessments_by_district_and_year(client, year=None, district_id=None):
    if district_id is None:
        district_id = client.preferences.district_id
    if year is None:
        year = client.preferences.year
    return export(client, 'AssessmentsByDistrictAndYear', year, district_id)

def intervention_records_by_district_and_year(client, year=None, district_id=None):
    if district_id is None:
        district_id = client.preferences.district_id
    if year is None:
        year = client.preferences.year
    return export(client, 'InterventionRecordsByDistrictAndYear', year, district_id)

def all_exports():
    return [fpc_assessments_by_district_and_year, assessments_by_district_and_year, intervention_records_by_district_and_year]