"""
components/random_picker.py — Random movie picker component.

Responsibilities:
- Picking a random movie from the watchlist
- Displaying the selected movie's details

Follows SRP: this component only handles the random movie picking logic.
Follows OCP: the picking logic is self-contained, so it can be easily modified without affecting other parts of the application.
"""

import streamlit as st
import random
from cache import get_title_details

def get_not_watched_movies(movies):
    """Filter the watchlist to return only movies that haven't been watched."""
    return [movie for movie in movies if not bool(int(movie["haveWatched"]))]

def get_random_title(movies):
    """Pick a random title from the provided list."""
    movie_list = get_not_watched_movies(movies)
    if not movie_list:
        st.warning("No movies available to pick from.")
        return None
    return random.choice(movie_list)['titleID']  # Assuming titleID can be used to fetch details

def render_random_picker(movies):
    """Render a random picker component."""

    if st.button("Pick a random movie", key="random_picker_btn"):
        random_title = get_random_title(movies)
        if random_title:
            title_name = get_title_details(random_title).get("original_title", "Unknown Title")
            title_runtime = get_title_details(random_title).get("runtime", "N/A")
            st.success(f"You should watch: {title_name} ({title_runtime} mins) !")
