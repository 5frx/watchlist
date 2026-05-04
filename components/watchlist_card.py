"""
components/watchlist_card.py — Watchlist entry card component.

Responsibilities:
- Rendering a single watchlist movie row (poster, details, watched checkbox, remove button)
- Handling watched status updates and movie removal interactions

Follows SRP: this component only renders and handles one watchlist row.
Follows OCP: new columns or interactions can be added here without
             modifying the watchlist page or other components.
"""

import streamlit as st
import data_store


def render_watchlist_card(movie: dict, title_details: dict, movies: list):
    """
    Render a single watchlist row with poster, metadata, watched toggle, and remove button.

    Args:
        movie:         The movie dict from the watchlist (contains titleID, haveWatched).
        title_details: The full title metadata returned from the API.
        movies:        The full watchlist, needed to save watched status changes.
    """
    col1, col2, col3, col4 = st.columns([1, 3, 1, 0.5])

    with col1:
        # Display poster or placeholder if unavailable
        if title_details.get("poster_path"):
            st.image("https://image.tmdb.org/t/p/w500" + title_details["poster_path"], width=100)
        else:
            st.write("No image available.")

    with col2:
        # Movie metadata
        st.header(title_details["original_title"])
        st.write(f"Release Year: {title_details.get('release_date', 'N/A')}")
        st.write(f"Runtime: {title_details.get('runtime', 'N/A')} minutes")
        # Display Netflix availability if available
        if title_details.get("netflix_link"):
            st.markdown(f"**Available on Netflix:** [Watch here]({title_details['netflix_link']})")

    with col3:
        # Watched checkbox — saves immediately on toggle
        current_watched = bool(int(movie["haveWatched"]))
        have_watched = st.checkbox("Watched", value=current_watched, key=f"watched_{movie['titleID']}")

        if have_watched != current_watched:
            movie["haveWatched"] = int(have_watched)
            data_store.save_movies(movies)
            st.success(f"Updated watched status for '{title_details['original_title']}'!")

    with col4:
        # Remove button — deletes this entry from the watchlist
        if st.button("X", key=movie["titleID"]):
            data_store.remove_movies([movie])
            st.success(f"Removed '{title_details['original_title']}' from watchlist!")