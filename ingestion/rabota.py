import os

from requests_html import HTMLSession
from sqlalchemy import create_engine, text

DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_NAME = os.environ['DATABASE_NAME']
DB_USER = os.environ['DATABASE_USER']
DB_HOST = os.environ['DATABASE_HOST']

engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME))
html_session = HTMLSession()

CITY_ID = '1'
DOMAIN_URL = 'https://www.rabota.md'
LANGUAGE = 'ro'
QUERY = 'Junior'

engine.execute(text(
    """
    CREATE TABLE IF NOT EXISTS `jobs` (
        `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(200) NOT NULL,
        `link` VARCHAR(200) NOT NULL,
        `status` VARCHAR(50) NOT NULL,
        `job_id` VARCHAR(50) NOT NULL,
        `favourite` BOOLEAN NOT NULL
    )
    """))


def normalize_link(link):
    # converts the link into full format
    if link.startswith('/ro'):
        return f'https://www.rabota.md{link}'
    else:
        return f'https:{link}'


def extract_job_id_from_link(link):
    """
    Extracts job_id from the specified link.
    :param link: link the job_id is extracted from
    :return: job identifier
    """
    job_id = link.split('id=')[-1].split('&')[0]
    if job_id.isdigit():
        return job_id

    job_id = link.split('/')[-1]
    if job_id.isdigit():
        return job_id

    raise Exception(f'Could not extract job_id from {link}...')


def parse_url(url):
    # extracts jobs from the specified link
    html_source = html_session.get(url).html

    data = []
    jobs = html_source.xpath('//div[@class="preview"]/h3/a[@class="vacancy"]')
    for job in jobs:
        link = job.xpath('//@href')[0]
        data.append({
            'name': job.text,
            'link': normalize_link(link),
            'job_id': extract_job_id_from_link(link),
        })

    return data


def run_ingestion():
    url = f'{DOMAIN_URL}/search?query={QUERY}&searchType=1&cityID={CITY_ID}&lang={LANGUAGE}'

    # get jobs from database
    db_jobs_ids_rows = engine.execute(text('SELECT job_id FROM jobs'))
    db_jobs_ids = [row.job_id for row in db_jobs_ids_rows]

    # scrape jobs from source
    scraped_jobs = []
    scraped_jobs_ids = []
    for page in range(1, 1000):
        page_data = parse_url(f'{url}&page={str(page)}')
        if not page_data:
            break

        scraped_jobs.extend(page_data)
        scraped_jobs_ids.extend([elm['job_id'] for elm in page_data])
        print(f'Parsed page {page}...')

    # find out new jobs and save them into databases as unseen
    new_jobs_ids = set(scraped_jobs_ids).difference(db_jobs_ids)
    if new_jobs_ids:
        new_jobs = [job for job in scraped_jobs if job['job_id'] in new_jobs_ids]
        engine.execute(text(f'INSERT INTO jobs(name, link, job_id, status, favourite) '
                            f'VALUES(:name, :link, :job_id, "unseen", {0})'),
                       new_jobs)
        print(f'New jobs: {len(new_jobs_ids)}...')

    # find out expired jobs and remove them from database
    expired_jobs_ids = set(db_jobs_ids).difference(scraped_jobs_ids)
    if expired_jobs_ids:
        engine.execute(text('DELETE FROM jobs WHERE id IN :jobs'), {'jobs': expired_jobs_ids})
        print(f'Expired jobs: {len(expired_jobs_ids)}...')

    print('Jobs parsed successfully...')


if __name__ == "__main__":
    run_ingestion()
