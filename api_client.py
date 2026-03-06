# import webbrowser

import requests
import json
# import time
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# watchmode_api_key = "MZyrPkUhS9fGm7PpnXwMFDKNNuPJ9uAfdAuBNOe9"
# WATCHMODE_URL_BASE = "https://api.watchmode.com/v1/"

# def create_robust_session():
#     """Creates a good request session with retry strategies"""
#     session = requests.Session()
    
#     retry_strategy = Retry(
#         total=3,
#         backoff_factor=1,
#         status_forcelist=[429,500,502,503,504],
#         allowed_methods=["GET"]
#     )

#     adapter=HTTPAdapter(
#         max_retries=retry_strategy,
#         pool_connections=10,
#         pool_maxsize=20
#     )
    
#     session.mount("http://",adapter)
#     session.mount("https://",adapter)
    
#     return session

# WATCHMODE_SESSION = create_robust_session()

# def getTitleIDs(titleName):
#     searchMovieResp = WATCHMODE_SESSION.get(URL_BASE + "search/?apiKey=" + api_key + "&search_field=name&search_value=" + titleName.replace(" ", "%20"))
#     searchMovieResp.raise_for_status()
#     searchMovieData = searchMovieResp.json()
#     return [result["id"] for result in searchMovieData["title_results"]]

# def getTitleDetails(titleID):
#     getTitleDetailResp = WATCHMODE_SESSION.get(URL_BASE + "title/" + str(titleID) + "/details/?apiKey=" + api_key)
#     getTitleDetailResp.raise_for_status()
#     return getTitleDetailResp.json()

API_KEY = st.secrets["tmdb"]["API_KEY"]   # v3 Auth (query param alternative)
BEARER_TOKEN = st.secrets["tmdb"]["BEARER_TOKEN"]  # v4 Auth (Authorization header)
URL_BASE = "https://api.themoviedb.org/3/"


def create_robust_session():
    """Creates a robust request session with retry strategies."""
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=20
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


TMDB_SESSION = create_robust_session()

# def createRequestToken():
#     headers = {
#     "accept": "application/json",
#     "Authorization": f"Bearer {BEARER_TOKEN}"}
#     resp = TMDB_SESSION.get(URL_BASE + "authentication/token/new", headers=headers)
#     resp.raise_for_status()
#     return resp.json().get("request_token")

# def askForPermission(requestToken):
#     url = "https://www.themoviedb.org/authenticate/" + requestToken
#     webbrowser.open(url)

# def createSession(requestToken):
#     headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     }
#     resp = TMDB_SESSION.post(URL_BASE + "authentication/session/new", headers=headers, json={"request_token": requestToken})
#     resp.raise_for_status()
#     return resp.json().get("session_id")

# def startAuthenticationFlow():
#     requestToken = createRequestToken()
#     askForPermission(requestToken)
#     # Wait for user to authenticate before proceeding
#     time.sleep(20)  # Adjust as needed for user interaction
#     sessionID = createSession(requestToken)
#     return sessionID

def getTitleIDs(titleName):
    params = {
        "api_key": API_KEY,
        "query": titleName
    }
    resp = TMDB_SESSION.get(URL_BASE + "search/movie", params=params)
    resp.raise_for_status()
    data = resp.json()
    return [result["id"] for result in data.get("results", [])]

def getTitleDetails(titleID):
    params = {
        "api_key": API_KEY
    }
    resp = TMDB_SESSION.get(URL_BASE + f"movie/{titleID}", params=params)
    resp.raise_for_status()
    return resp.json()
