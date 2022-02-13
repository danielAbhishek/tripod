
from faker import Faker
import random
from datetime import date, datetime, timedelta


def get_job_data(users, events):
    """
    creating fake data,
    * need five users
    * need five events
    """
    faker = Faker()
    data = {}
    seed = 0
    jobs = ['Weeding_job', 'Birthday_job', 'pre-shoot_job']
    for job in jobs:
        faker.seed(seed)
        inner_data = data[job]
        inner_data = {}
        inner_data['job_name'] = job
        inner_data['primary_client'] = users[random.randint(0, 4)]
        inner_data['secondary_client'] = users[random.randint(0, 4)]
        inner_data['event'] = events[random.randint(0, 4)]
        inner_data['venue'] = faker.street_address()
        inner_data['venue_notes'] = faker.paragraph(nb_sentences=2)
        start_date = faker.date_between(
            start_date=date.today(),
            end_date= date.today(), + timedelta(days=30)
        )
        end_date = start_date + timedelta(days=random.randint(0, 30))
        inner_data['start_date'] = start_date
        inner_data['end_date'] = end_date
        all_day = True if seed % 2 == 0 else False
        start_time = faker.time_object() if 
        seed += 1
