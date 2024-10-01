import os
from dotenv import load_dotenv  
from google_sheets_manager import GoogleSheetsManager, clean_spreadsheet_id
from data_manager import DataManager
from job_application import JobApplication

def main():
    load_dotenv()

    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    spreadsheet_id = clean_spreadsheet_id(os.getenv("GOOGLE_SPREADSHEET_ID", ""))
    
    # Remove any potential angle brackets from the spreadsheet_id
    spreadsheet_id = spreadsheet_id.strip('<>')

    print(f"Credentials path: {credentials_path}")
    print(f"Spreadsheet ID: {spreadsheet_id}")

    sheets_manager = GoogleSheetsManager(credentials_path, spreadsheet_id)
    data_manager = DataManager(sheets_manager)

    while True:
        print("\nJob Application Tracker")
        print("1. Add a new job application")
        print("2. View all job applications")
        print("3. Update a job application status")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_new_job_application(data_manager)
        elif choice == "2":
            view_all_job_applications(data_manager)
        elif choice == "3":
            update_job_status(data_manager)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def add_new_job_application(data_manager):
    title = input("Job Title: ")
    company = input("Company: ")
    job_req = input("Job Req #: ")
    url = input("Job URL: ")
    location = input("Location: ")
    job_type = input("Job Type: ")
    date_applied = input("Date Applied (YYYY-MM-DD): ")
    deadline = input("Application Deadline (YYYY-MM-DD): ")
    description = input("Job Description: ")
    status = input("Application Status (Applied, Interview, etc.): ")

    job = JobApplication(title, company, job_req, url, location, job_type, date_applied, deadline, description, status)
    data_manager.add_job_application(job)
    print("Job application added successfully.")

def view_all_job_applications(data_manager):
    jobs = data_manager.load_job_applications()
    if not jobs:
        print("No job applications found.")
    else:
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job.title} at {job.company}")
            print(f"    Status: {job.status}")
            print(f"    Applied on: {job.date_applied}")

def update_job_status(data_manager):
    job_req = input("Enter the Job Requisition Number: ")
    new_status = input("Enter the new status: ")
    data_manager.update_job_status(job_req, new_status)
    print("Job application status updated successfully.")

if __name__ == "__main__":
    main()