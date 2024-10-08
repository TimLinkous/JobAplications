import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
from job_application import JobApplication
from datetime import date, datetime
import ast
from dotenv import load_dotenv

load_dotenv()

def clean_spreadsheet_id(id_string: str) -> str:
    """Remove angle brackets and any surrounding whitespace from the spreadsheet ID."""
    return re.sub(r'^\s*<?\s*|\s*>?\s*$', '', id_string)

credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
spreadsheet_id = clean_spreadsheet_id(os.getenv("GOOGLE_SPREADSHEET_ID", ""))

spreadsheet_id = spreadsheet_id.strip('<>')


class GoogleSheetsManager:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.spreadsheet_id = clean_spreadsheet_id(spreadsheet_id)
        self.spreadsheet_id = spreadsheet_id.strip('<>')  # Remove any potential angle brackets
        print(f"Initializing GoogleSheetsManager with spreadsheet ID: {self.spreadsheet_id}")
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes = ['https://www.googleapis.com/auth/spreadsheets'])
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def read_sheet(self, range_name: str) -> List[List]:
        try:
            print(f"Attempting to read sheet with ID: {self.spreadsheet_id}")
            result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id, range = range_name).execute()
            return result.get('values', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def write_sheet(self, range_name: str, values: List[List]):
        try:
            print(f"Attempting to write to sheet with ID: {self.spreadsheet_id}")
            body = {'values': values}
            result = self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated")
        except HttpError as error:
            print(f"An error occurred while writing to the sheet: {error}")
            

    def append_sheet(self, range_name: str, values: List[List]):
        try:
            body = {'values': values}
            result = self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updates').get('updatedCells')} cells appended")
        except HttpError as error:
            print(f"An error occurred: {error}")
            
    def clear_sheet(self, range_name: str):
        try:
            self.sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
            print(f"Range {range_name} cleared.")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def job_application_to_row(self, job: JobApplication) -> List:
        return [
            job.title, job.company, job.url, job.location, job.job_type,
            str(job.date_applied), str(job.deadline), job.description, job.status,
            ', '.join(map(str, job.follow_up_dates)),
            str(job.last_activity),
            str(job.contact_info),
            str(job.interview_info),
            str(job.salary_info),
            str(job.documents)
        ]

    def row_to_job_application(self, row: List) -> JobApplication:
        job = JobApplication(*row[1:10])  # first 9 elements
        job.job_req = row[0]
        job.follow_up_dates = [date.fromisoformat(d.strip()) for d in row[10].split(',')] if row[10] else[]
        job.last_activity = date.fromisoformat(row[11] if row[11] else None)
        job.contact_info = ast.literal_eval(row[12]) if row[12] else {}
        job.interview_info = eval(row[13]) if row[13] else {}
        job.salary_info = eval(row[14]) if row[14] else {}
        job.documents = eval(row[15]) if row[15] else {}
        return job

    def sync_job_applications(self, jobs: List[JobApplication]):
        header = ['Job Req #', 'Title', 'Company', 'URL', 'Location', 'Job Type', 'Date Applied', 'Deadline', 'Description', 'Status', 'Follow-up Dates', 'Last Activity', 'Contact Info', 'Interview Info', 'Salary Info', "Documents"]
        values = [header] + [self.job_application_to_row(job) for job in jobs]
        self.clear_sheet('A1:P')
        self.write_sheet('A1:P', values)

    def get_job_applications(self) -> List[JobApplication]:
        data = self.read_sheet('A2:P')
        return [self.row_to_job_application(row) for row in data]
    
sheets_manager = GoogleSheetsManager(credentials_path, spreadsheet_id)
