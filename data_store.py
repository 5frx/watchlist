import csv
import json

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_sheet():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(st.secrets["google_sheets"]["sheet_url"])
    return sheet.worksheet("movies")

def load_movies():
    sheet = get_sheet()
    movies = sheet.get_all_records()
    return movies

def save_movies(movies):
    sheet = get_sheet()
    sheet.clear()
    rows = [["haveWatched", "titleID"]]
    rows += [[m["haveWatched"], m["titleID"]] for m in movies]
    sheet.update("A1", rows)  # Single write request instead of one per row
    
def add_movies(movies_list):
    sheet = get_sheet()
    rows = [[m["haveWatched"], m["titleID"]] for m in movies_list]
    sheet.append_rows(rows)  # Single request for all rows

def remove_movies(movies_list):
    movies = load_movies()
    remove_ids = {movie['titleID'] for movie in movies_list}
    updated_movies = [movie for movie in movies if movie['titleID'] not in remove_ids]
    save_movies(updated_movies)

# def load_movies():
#     with open('movies.csv', 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         movies = [row for row in reader]
    
#     return movies

# def save_movies(movies):
#     with open('movies.csv', 'w', newline='') as csvfile:
#         fieldnames = ['haveWatched', 'titleID']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
#         writer.writeheader()
#         for movie in movies:
#             writer.writerow(movie)

# def add_movies(movies_list):
#     movies = load_movies()
#     movies.extend(movies_list)
#     save_movies(movies)

# def remove_movies(movies_list):
#     movies = load_movies()
#     movies = [movie for movie in movies if movie not in movies_list]
#     save_movies(movies)

# def update_movie_ids(movies):
#     for movie in movies:
#         title_ids = api_client.getTitleIDs(movie["title"])
#         if title_ids:
#             movie["titleID"] = title_ids[0]  # Use the first ID found
#     save_movies(movies)
#     print("Update complete: Movie IDs have been updated.")

# update_movie_ids(load_movies())  # Ensure all movies have their titleID updated