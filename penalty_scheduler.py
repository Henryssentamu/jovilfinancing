import schedule
import time
from DatabaseClasses import Penalties_Overdues

def run_penalty_overdue_job():
    obj = Penalties_Overdues()
    obj.make_zero_payments()
    print("Penalty and overdue job run successfully.")

def start_scheduler():
    schedule.every().day.at("10:48").do(run_penalty_overdue_job)

    while True:
        schedule.run_pending()
        time.sleep(30)
