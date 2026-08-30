import json
import requests


def load_schedule(session, start_date: str) -> str:
    """Fetch one week of league-wide schedule data (all 32 teams) starting
    at start_date, land it raw into RAW.SCHEDULE, and return the API's
    nextStartDate so callers can chain forward if needed.

    start_date: "YYYY-MM-DD" or "now" for the current week.

    Requires NHL_API_ACCESS_INTEGRATION to be attached as an
    EXTERNAL_ACCESS_INTEGRATION when this proc is created.
    """
    url = f"https://api-web.nhle.com/v1/schedule/{start_date}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    session.sql(
        "INSERT INTO RAW.SCHEDULE (raw_json, source_url) "
        "SELECT PARSE_JSON(?), ?",
        params=[json.dumps(payload), url],
    ).collect()

    return payload["nextStartDate"]