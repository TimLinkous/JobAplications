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
        try:
            result = self.sheet.values().get(spreadsheet_ID=self.spreadsheet_id, range = range_name).execute()
            return result.get('values', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def write_sheet(self, range_name: str, values: List[List]):
        try:
            body = {'values': values}
            result = self.sheet.values().update(
                spreadsheet_ID=self.spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def append_sheet(self, range_name: str, values: List[List]):
        try:
            body = {'values': values}
            result = self.sheet.values().append(
                spreadsheet_ID=self.spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updates').get('updatedCells')} cells appended")
        except HttpError as error:
            print(f"An error occurred: {error}")
            

    def clear_sheet(self, range_name: str):
        try:
            self.sheet.values().clear(spreadsheet_ID=self.spreadsheet_id, range=range_name).execute()
            print(f"Range {range_name} cleared.")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def job_application_to_row(self, job: JobApplication) -> List:
        pass

    def row_to_job_application(self, row: List) -> JobApplication:
        pass

    def sync_job_applications(self, jobs: List[JobApplication]):
        pass

    def get_job_applications(self) -> List[JobApplication]:
        pass