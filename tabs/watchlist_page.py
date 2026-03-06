"""
pages/watchlist_page.py — Watchlist page rendering.

Responsibilities:
- Loading movies from storage
- Iterating over the watchlist and delegating card rendering
- Saving changes back to storage when triggered

Follows SRP: this module only handles watchlist page layout and flow.
Follows OCP: the per-movie display is fully delegated to the watchlist
             card component, so card changes don't touch this file.
"""

import streamlit as st
import data_store
from components.watchlist_card import render_watchlist_card
from components.random_picker import render_random_picker
from cache import get_title_details


def render():
    """Render the watchlist page."""
    movies = data_store.load_movies()

    if not movies:
        st.write("Your watchlist is empty.")
        return

    st.write("Your Watchlist:")

    render_random_picker(movies)
    
    for movie in movies:
        try:
            title_details = get_title_details(movie["titleID"])  # cached API call
        except Exception:
            st.warning(f"Failed to retrieve details for movie ID {movie['titleID']}")
            continue

        # Delegate all per-movie UI and interaction to the watchlist card component
        
        render_watchlist_card(movie, title_details, movies)