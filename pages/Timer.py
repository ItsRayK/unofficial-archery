#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Function to get query parameters
def get_range_name():
    query_params = st.experimental_get_query_params()
    return query_params.get("range", ["Unofficial Archery"])[0]

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯")

### Apply Custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Session State   #
#-------------------#
if 'setup_time' not in st.session_state:
    st.session_state['setup_time'] = 10

if 'shooting_time' not in st.session_state:
    st.session_state['shooting_time'] = 90

if 'num_practice_ends' not in st.session_state:
    st.session_state['num_practice_ends'] = 2

if 'num_scoring_ends' not in st.session_state:
    st.session_state['num_scoring_ends'] = 10

if 'is_double_line' not in st.session_state:
    st.session_state['is_double_line'] = False

#-------------------#
#   Page Elements   #
#-------------------#

###################### DEBUG ################
st.session_state