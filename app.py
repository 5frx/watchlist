"""
app.py — Entry point for the Watchlist Streamlit app.

Responsibilities:
- Page configuration
- Rendering the persistent title and navbar
- Routing to the correct page based on session state

Follows SRP: this file only handles app-level layout and routing.
Follows OCP: new pages can be added to the PAGES registry without
             modifying existing routing logic.
"""

import streamlit as st
from tabs.search_page import render as render_search
from tabs.watchlist_page import render as render_watchlist

# ---------------------------------------------------------------------------
# Page registry — add new pages here without touching routing logic (OCP)
# ---------------------------------------------------------------------------
PAGES = {
    "search":    {"label": "Search for Movies/TV Shows", "render": render_search},
    "watchlist": {"label": "My Watchlist",               "render": render_watchlist},
}

# ---------------------------------------------------------------------------
# App config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="My Watchlist", page_icon="🎬", layout="wide")

# ---------------------------------------------------------------------------
# Persistent title — always visible regardless of active page
# ---------------------------------------------------------------------------
st.title("My Watchlist")
st.divider()

# ---------------------------------------------------------------------------
# Navbar — one button per registered page
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "search"

nav_cols = st.columns(len(PAGES))
for col, (page_key, page_cfg) in zip(nav_cols, PAGES.items()):
    with col:
        if st.button(page_cfg["label"], use_container_width=True):
            st.session_state.page = page_key

st.divider()

# ---------------------------------------------------------------------------
# Page routing — delegate rendering to the active page module
# ---------------------------------------------------------------------------
active_page = PAGES.get(st.session_state.page)
if active_page:
    active_page["render"]()