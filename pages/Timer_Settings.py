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

## Setup Two Column Layout
col1, col2 = st.columns(2)

## Column 1 Elements
num_practice_ends = col1.number_input("# Practice Ends", min_value=0, value=st.session_state['num_practice_ends'], step=1, format="%d")
setup_time = col1.number_input("Setup Time (Seconds)", min_value=0, value=st.session_state['setup_time'], step=1, format="%d")

is_double_line = col1.checkbox("Double Line", value=st.session_state['is_double_line'])

## Column 2 Elements
num_scoring_ends = col2.number_input("# Scoring Ends", min_value=0, value=st.session_state['num_scoring_ends'], step=1, format="%d")
shooting_time = col2.number_input("Shooting Time (Seconds)", min_value=0, value=st.session_state['shooting_time'], step=1, format="%d")

## "Apply" Button to Save Session State
if col1.button("Apply"):
    # Save Number of Ends
    st.session_state['num_practice_ends'] = num_practice_ends
    st.session_state['num_scoring_ends'] = num_scoring_ends

    # Save Time Settings
    st.session_state['setup_time'] = setup_time
    st.session_state['shooting_time'] = shooting_time

    # Save Flags
    st.session_state['is_double_line'] = is_double_line

    # Reload Page
    st.rerun()

#-------------------------------------------------#
###################### DEBUG ######################
#-------------------------------------------------#
st.session_state