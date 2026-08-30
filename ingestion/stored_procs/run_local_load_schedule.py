"""
Runs load_schedule() directly on your machine -- no deployed stored
procedure involved. Tests a single week's league-wide schedule pull.

Usage (from this directory):
    python run_local_load_schedule.py --date 2024-10-08
    python run_local_load_schedule.py --date now
"""
import argparse

from load_schedule_proc import load_schedule
from local_session import get_local_session

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="YYYY-MM-DD or 'now'")
    args = parser.parse_args()

    session = get_local_session()
    try:
        result = load_schedule(session, args.date)
        print(f"Loaded week starting {args.date}. Next start date: {result}")
    finally:
        session.close()