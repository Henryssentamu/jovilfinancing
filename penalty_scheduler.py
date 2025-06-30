import schedule
import time
from DatabaseClasses import Penalties_Overdues

def run_penalty_overdue_job():
    obj = Penalties_Overdues()
    obj.total_penalties_and_oversdues_triger()
    obj.insert_penalties_and_overdues()
    print("Penalty and overdue job run successfully.")

def start_scheduler():
    schedule.every().day.at("16:10").do(run_penalty_overdue_job)

    while True:
        schedule.run_pending()
        time.sleep(30)
