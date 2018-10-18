from . import BASE_URL, HTTP_ERROR
from dateutil import parser
import re

class ExportFile:
    def __init__(self, data, filename, filedate):
        self.data = data
        self.filename = filename
        self.filedate = filedate

def clean_export_data(export_data):
    """Export data has a text qualifier: ="{data}", this strips them out"""
    regex_pattern = r'="([^\"]*)"'
    regex_replacement = r'\1' ## capture group 1 == the actual str
    export_data_clean = re.sub(regex_pattern, regex_replacement, export_data)
    return export_data_clean

def extract_export_filename(export_headers):
    """
    """
    filename_pattern = 'attachment; filename="(.*)"'
    filename_match = re.match(
            filename_pattern,
            export_headers['Content-Disposition']
        )
    filename = filename_match.group(1)
    return filename

def export(client, endpoint, year, district_id):
    export_url = f'{BASE_URL}/export/{endpoint}/{district_id}'
    querystring = {'year': year}

    try:
        export_response = client.session.get(export_url, params=querystring)
        export_response.raise_for_status()
    except HTTP_ERROR as err:
        print(err)

    if export_response.ok:
        export_data_clean = clean_export_data(export_response.text)

        export_filename = extract_export_filename(export_response.headers)

        export_filedate = export_response.headers['Date']
        export_filedate_parsed = parser.parse(export_filedate)
        export_filedate_iso = export_filedate_parsed.isoformat()

        return ExportFile(
                data=export_data_clean,
                filename=export_filename,
                filedate=export_filedate_iso
            )

def fpc_assessments_by_district_and_year(client, year=None, district_id=None):
    endpoint = 'FPCAssessmentsByDistrictAndYear'
    if district_id is None:
        district_id = client.district_id
    if year is None:
        year = client.default_school_year
    return export(client, endpoint, year, district_id)

def assessments_by_district_and_year(client, year=None, district_id=None):
    endpoint = 'AssessmentsByDistrictAndYear'
    if district_id is None:
        district_id = client.district_id
    if year is None:
        year = client.default_school_year
    return export(client, endpoint, year, district_id)

def intervention_records_by_district_and_year(client, year=None, district_id=None):
    endpoint = 'InterventionRecordsByDistrictAndYear'
    if district_id is None:
        district_id = client.district_id
    if year is None:
        year = client.default_school_year
    return export(client, endpoint, year, district_id)

def all_exports():
    return [fpc_assessments_by_district_and_year, assessments_by_district_and_year, intervention_records_by_district_and_year]