from google_sheets_manager import GoogleSheetsManager
from job_application import JobApplication

class DataManager:
    def __init__(self, sheets_manager: GoogleSheetsManager):
        self.sheets_manager = sheets_manager

    def load_job_applications(self):
        """Load all job applications from Google Sheets."""
        return self.sheets_manager.get_job_applications()

    def save_job_applications(self, jobs: list[JobApplication]):
        """Sync job applications with Google Sheets."""
        self.sheets_manager.sync_job_applications(jobs)

    def add_job_application(self, job: JobApplication):
        """Add new job application to Google Sheets."""
        job_applications = self.load_job_applications()
        job_applications.append(job)
        self.save_job_applications(job_applications)

    def update_job_status(self, job_req_number, new_status):
        """Update the status of a specific job application."""
        job_applications = self.load_job_applications()
        for job in job_applications:
            if job.job_req == job_req_number:
                job.update_status(new_status)
                break
        self.save_job_applications(job_applications)

    def clear_all_job_applications(self):
        """Clear all job applications from Google Sheets."""
        self.sheets_manager.clear_sheet('A2:P')