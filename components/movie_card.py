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
    print(f"Fetched details for titleID {title_id}: {title_details}")  # Debug log
    netflix_link = api_client.getNetflixLink(title_id)
    col1, col2, col3 = st.columns([1, 3, 1])

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
                "titleID": title_id,
                "netflix": netflix_link if netflix_link else "",
            }])
            st.success(f"Added '{title_details['original_title']}' to watchlist!")
        # Display Netflix availability if available
    with col3:
        if netflix_link:
            st.write(f"**Available on Netflix:** [Watch here]({netflix_link})")
        else:
            st.write("Not available on Netflix.")
