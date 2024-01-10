from src.classes.database import Database
from src.scrappers.kariyernet import KariyerNetJobScraper
from src.scrappers.myjobmu import MyJobMuJobScraper
from src.analyser.runner import update_analytics
from src.utils.service_key import get_service_account_key
from src.badge_generator import update_job_count_badge
import argparse


def get_args():
    """
    Returns command line arguments.

    :returns
        args (argparse.Namespace): command line arguments
    """
    parser = argparse.ArgumentParser(description='Scrape IT jobs from different job portals')
    parser.add_argument('website', type=str,
                        help='website to scrape jobs from')
    parser.add_argument('--max_jobs', type=int,
                        help='maximum number of jobs to scrape')
    args = parser.parse_args()
    return args


def rebase_stats() -> None:
    """
    After DELETING the `statistics` collection in main database and frontend
    database manually, call this function to recalculate all statistics
    and sync with `frontend-db`.

    No scraping takes place when this function is called. Statistics are
    calculated from existing scraped jobs.

    ! DO NOT CALL THIS FUNCTION AT THE SAME TIME AS main()
    ! WARNING: This function heavily impacts read and write quotas.
    """
    # load main database.
    main_db = Database(get_service_account_key(forMainDB=True))

    # get all jobs stored in database
    all_jobs = main_db.get_dataframe().to_dict('records')

    # update general stats
    main_db.update_metadata(len(all_jobs))

    if (len(all_jobs) == 0):
        sync_stats(main_db)
        return

    # get data to be analysed in a list
    job_details_list = [job['job_details'] for job in all_jobs]
    salary_list = [job['salary'] for job in all_jobs]
    location_list = [job['location'] for job in all_jobs]
    job_title_list = [job['job_title'] for job in all_jobs]

    # process data and updates statistics
    update_analytics(main_db, job_title_list,
                     job_details_list, location_list, salary_list)
    main_db.update_job_count_trend()

    # serve stats to frontend
    sync_stats(main_db)

    # update job count in readme
    update_job_count_badge(len(all_jobs))


def sync_stats(main_db: Database):
    """
    Clones statistics found in `main_db` to `frontend_db`

    Args:
        main_db (Database): database containing scraped data
    """
    frontend_db = Database(get_service_account_key(), "frontend_db")
    x = main_db.export_collection(main_db.stats_collection_ref)
    frontend_db.import_collection(frontend_db.stats_collection_ref, x)


def backup_to_drive():
    """
    Saves all jobs in main database to google drive in json format.
    """
    # TODO: complete function
    main_db = Database(get_service_account_key(forMainDB=True))
    df = main_db.get_dataframe()
    df.to_json('sample_jobs.json', orient='records')


def main():
    """
    Driver code.

    ! Do not call this function together with rebase_stats in
    ! the same program.
    """
    # get command line arguments
    args = get_args()
    website = args.website
    max_jobs = args.max_jobs

    # setup database and scraper.
    main_db = Database(get_service_account_key(forMainDB=True))

    my_scraper = None

    if website == 'myjobmu':
        my_scraper = MyJobMuJobScraper(main_db.get_recent_urls(), limit=max_jobs)
    elif website == 'kariyernet':
        my_scraper = KariyerNetJobScraper(main_db.get_recent_urls(), limit=max_jobs)

    # fetch new jobs from specified website
    new_jobs = my_scraper.scrape()

    # if no new jobs found exit
    if (len(new_jobs) == 0):
        return

    # get data to be analysed in a list
    job_details_list = [job['job_details'] for job in new_jobs]
    salary_list = [job['salary'] for job in new_jobs]
    location_list = [job['location'] for job in new_jobs]
    job_title_list = [job['job_title'] for job in new_jobs]

    # print some info about new jobs found
    print(len(new_jobs), ' new jobs found!')
    print(job_title_list[:5])

    # update database general stats such as size and last update dates
    new_db_size = main_db.get_size() + len(new_jobs)
    main_db.update_metadata(new_db_size)

    # save new jobs to database
    for job in new_jobs:
        main_db.add_job(job)

    # extract statistics from newly scraped data and update
    # statistics collection
    update_analytics(main_db, job_title_list,
                     job_details_list, location_list, salary_list)
    main_db.update_job_count_trend()

    # send updated statistics to frontend db
    sync_stats(main_db)

    # update job count in readme
    update_job_count_badge(new_db_size)


if __name__ == "__main__":
    main()
