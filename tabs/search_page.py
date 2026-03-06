"""
pages/search_page.py — Search page rendering.

Responsibilities:
- Rendering the movie/TV show search input
- Displaying search results by delegating to the movie card component

Follows SRP: this module only handles search page layout and flow.
Follows OCP: result display is delegated to components, so new display
             formats can be added without modifying this file.
"""
import streamlit as st
import api_client
from components.movie_card import render_search_card

def render():
    """Render the search page."""
    title_name = st.text_input("Enter a movie: ")

    if not title_name:
        return

    try:
        title_ids = api_client.getTitleIDs(title_name)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return

    if not title_ids:
        st.write("No results found.")
        return

    # Show how many results were found and how many are displayed
    result_count = len(title_ids)
    display_count = min(5, result_count)
    st.write(f"Found {result_count} results. Showing details for 1 - {display_count}:")

    # Render a card for each of the first 5 results
    for title_id in title_ids[:5]:
        render_search_card(title_id)