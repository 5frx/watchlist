"""
cache.py — Cached wrappers around API calls.

Responsibilities:
- Wrapping expensive API calls with Streamlit's cache to avoid redundant
  network requests on every rerun

Follows SRP: this module only owns caching concerns — it does not contain
             business logic, UI, or storage logic.
Follows OCP: new cached API calls can be added here without modifying
             any page or component that consumes them.
"""

import streamlit as st
import api_client


@st.cache_data
def get_title_details(title_id: str) -> dict:
    """
    Fetch and cache title details for a given ID.

    The result is stored in Streamlit's cache keyed by title_id, so
    subsequent reruns skip the network call entirely.

    Args:
        title_id: The unique ID of the title to look up.

    Returns:
        A dict of title metadata from the API.
    """
    return api_client.getTitleDetails(title_id)