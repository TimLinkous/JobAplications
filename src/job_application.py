from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

class JobApplication:
    def __init__(self, title, company, url, location, job_type, date_applied, deadline, description, status):
        self.title = title
        self.company = company
        self.url = url
        self.location = location
        self.job_type = job_type
        self.date_applied = date_applied
        self.deadline = deadline
        self.description = description
        self.status = status
        self.follow_up_dates = []
        self.last_activity = None
        self.contact_info = {}
        self.interview_info = {}
        self.salary_info = {}
        self.documents = {}

    def add_follow_up_date(self, date):
        self.follow_up_dates.append(date)

    def update_status(self, status):
        self.status = status

    def update_contact_info(self, name, phone, email):
        self.contact_info[name] = {'name': name, 'phone': phone, 'email': email}