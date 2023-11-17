import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter


def add_retries_to_requests_session(
    session, retries=3, backoff_factor=0.3, status_forcelist=(502, 503, 504)
):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)


def requests_session_with_retries(
    retries=3, backoff_factor=0.3, status_forcelist=(502, 503, 504)
):
    session = requests.Session()
    add_retries_to_requests_session(
        session,
        retries=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    return session
