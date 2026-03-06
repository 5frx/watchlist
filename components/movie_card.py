"""
components/movie_card.py — Search result movie card component.

Responsibilities:
- Fetching and displaying title details for a single search result
- Handling the "Add to Watchlist" button interaction

Follows SRP: this component only renders a single search result card.
Follows OCP: poster display and button behaviour are self-contained,
             so new fields can be added here without touching the page.
"""

import streamlit as st
import api_client
import data_store

def render_search_card(title_id: str):
    """
    Render a single search result card with poster and add-to-watchlist button.

    Args:
        title_id: The unique ID of the title to display.
    """
    title_details = api_client.getTitleDetails(title_id)

    col1, col2 = st.columns([1, 3])

    with col1:
        # Display poster if available, otherwise show a placeholder message
        if title_details.get("poster_path"):
            st.image("https://image.tmdb.org/t/p/w500" + title_details["poster_path"], width=150)
        else:
            st.write("No image available.")

    with col2:
        # Button to add this title to the watchlist
        if st.button(f"Add '{title_details['original_title']}' to watchlist", key=title_id):
            data_store.add_movies([{
                "haveWatched": 0,
                "titleID": title_id
            }])
            st.success(f"Added '{title_details['original_title']}' to watchlist!")
