import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
from job_application import JobApplication

class GoogleSheetsManager:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = service_account.Credentials.from_serice_account_file(credentials_path, scopes = ['https://www.googleapis.com/auth/spreadsheets'])
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def read_sheet(self, range_name: str) -> List[List]:
        pass

    def write_sheet(self, range_name: str, values: List[List]):
        pass

    def append_sheet(self, range_name: str, values: List[List]):
        pass

    def clear_sheet(self, range_name: str):
        pass

    def job_application_to_row(self, job: JobApplication) -> List:
        pass

    def row_to_job_application(self, row: List) -> JobApplication:
        pass

    def sync_job_applications(self, jobs: List[JobApplication]):
        pass

    def get_job_applications(self) -> List[JobApplication]:
        pass