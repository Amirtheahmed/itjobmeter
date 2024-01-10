from __future__ import annotations

import math
import os

import requests
from requests import Session
import time
from tqdm import tqdm
from datetime import datetime

from src.base_scrapper import BaseScraper
from src.classes.job import Job
from src.proxy_manager import ProxyManager

class KariyerNetJobScraper(BaseScraper):
    """
    Scrapes IT jobs from kariyer.net website
    """

    turkish_months = {
        'Ocak': 'January',
        'Şubat': 'February',
        'Mart': 'March',
        'Nisan': 'April',
        'Mayıs': 'May',
        'Haziran': 'June',
        'Temmuz': 'July',
        'Ağustos': 'August',
        'Eylül': 'September',
        'Ekim': 'October',
        'Kasım': 'November',
        'Aralık': 'December'
    }

    def __init__(self, scraped_ids: list[str], limit: int = -1) -> None:
        """
        Creates an instance of a scraper.

        Args:
            scraped_ids (list): A list of job URLs previously scraped. These
            jobs will be skipped. If an empty list is passed, all jobs found
            will be processed.

            limit (int): Maximum number of jobs that must be scraped. Default
            value of -1 means there's no limit.
        """

        self.scraped_job_ids: list[str] = scraped_ids

        self.limit: int = limit

        # default url for IT jobs sorted by most recent
        self.default_url: str = 'https://api-web.kariyer.net/search'

        # duration of loading page animation
        self.load_duration: int = 5  # ! Avoid decreasing this value

        # setup scraper
        proxy_manager = ProxyManager()
        super().__init__(proxy_manager)
        self.proxied: bool = os.environ.get('KARIYERNET_PROXIED', False)
        self.session: Session = requests.Session()

        # store new jobs found
        self.new_jobs: list[Job] = []

    def get_jobs_on_page(self, pageNumber: int) -> int:
        """
        Extracts all job data on a page and saves this
        data to `new_jobs`.

        Args:
            pageNumber(int): Page number

        Returns:
            int: number of new jobs scraped on current page
        """
        body: dict = {
            "memberId": 0,
            "currentPage": pageNumber,
            "size": 50,
            "departments": [
                "55",
                "78"
            ],
            "sortType": "SortByDate",
            "sortDirection": "Descending"
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = self.http_post(session=self.session, url=self.default_url, body=body, headers=headers, proxied=self.proxied)
        jobs = response.json()['data']['jobs']['items']

        # initialise counter for the number of new
        # jobs found on current page
        jobs_added_count = 0

        for job_module in tqdm(jobs):
            jobObj = Job()

            # get url and id of current job module
            jobObj.ad_id = job_module['id']

            # ignore already scraped jobs
            if jobObj.ad_id in self.scraped_job_ids:
                continue

            # else new job found
            jobs_added_count += 1
            self.scraped_job_ids.append(jobObj.ad_id)

            # get job from api
            response = self.http_get(
                session=self.session,
                url='https://api-web.kariyer.net/job?jobId={jobId}'.format(jobId=jobObj.ad_id),
                proxied=self.proxied)
            jobDetails = response.json()['data']

            # extract job title
            jobObj.job_title = jobDetails['jobGeneralInformation']['title']

            # extract company name
            # * Some job posts have `Hidden Company` as their company name
            # * and in this case, the required element is missing.
            if jobDetails['jobGeneralInformation']['confidential'] is True:
                jobObj.company = "Unknown"
            else:
                jobObj.company = jobDetails['jobCompanyInformation']['companyName'].strip()

            # extract date posted and closing date
            date_posted = jobDetails['jobGeneralInformation']['postingDate']

            closing_date = jobDetails['jobGeneralInformation']['closingDate']

            # convert string dates to correct datetime data type
            jobObj.date_posted =  datetime.strptime(date_posted, '%Y-%m-%d')
            for tr_month, en_month in self.turkish_months.items():
                closing_date = closing_date.replace(tr_month, en_month)

            jobObj.closing_date = datetime.strptime(closing_date, '%d %B %Y')

            # extract job location
            jobObj.location = jobDetails['jobGeneralInformation']['locationText']

            # extract salary
            jobObj.salary = "Unknown"

            # job details
            jobObj.job_details = jobDetails['jobGeneralInformation']['qualifications']

            # job ad language
            jobObj.job_ad_language = jobDetails['jobGeneralInformation']['language']

            # save job to list of scraped jobs
            self.new_jobs.append(jobObj)

            if len(self.new_jobs) == self.limit:
                return jobs_added_count

        return jobs_added_count

    def wait(self) -> None:
        """
        Wait for page to stop loading.
        """
        time.sleep(self.load_duration)

    def scrape(self) -> list[dict]:
        """
        Start scraping from first page.

        Raises:
            Exception: Unable to find number of pages

        Returns:
            list[dict]: New jobs found.
        """

        # fetch page count
        body: dict = {
            "memberId": 0,
            "currentPage": 1,
            "size": 50,
            "departments": [
                "55",
                "78"
            ],
            "sortType": "SortByDate",
            "sortDirection": "Descending"
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = self.http_post(session=self.session, url=self.default_url, body=body, headers=headers, proxied=self.proxied)
        data = response.json()
        totalJobs = data['data']['totalJobCount']
        last_page = math.ceil(totalJobs/50)

        # scrape each page
        for pageNumber in tqdm(range(1, last_page+1)):
            # extract job data
            jobs_added_count = self.get_jobs_on_page(pageNumber)

            # since jobs are sorted by recent, as soon as
            # we encounter a page which has already been visited we can stop
            # scraping. (all pages after current page are also already visited)
            if jobs_added_count == 0 or jobs_added_count == self.limit:
                break

        return [x.__dict__ for x in self.new_jobs]


if __name__ == "__main__":
    x = KariyerNetJobScraper([], 1)
    jobs = x.scrape()
    print(len(jobs))
    print(jobs[0])
