#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st
from math import ceil

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / ".." / "style" / "style.css"
ASSETS = THIS_DIR / ".." / "assets"

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯")

### Apply Custom CSS
#with open(CSS_FILE) as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Session State   #
#-------------------#
if 'setup_time' not in st.session_state:
    st.session_state['setup_time'] = 10

if 'shooting_time' not in st.session_state:
    st.session_state['shooting_time'] = 90

if 'low_time_warning' not in st.session_state:
    st.session_state['low_time_warning'] = 30

if 'low_time_urgent' not in st.session_state:
    st.session_state['low_time_urgent'] = 15

if 'use_warning_color' not in st.session_state:
    st.session_state['use_warning_color'] = True

if 'use_urgent_color' not in st.session_state:
    st.session_state['use_urgent_color'] = True

if 'num_practice_ends' not in st.session_state:
    st.session_state['num_practice_ends'] = 2

if 'num_scoring_ends' not in st.session_state:
    st.session_state['num_scoring_ends'] = 10

if 'is_double_line' not in st.session_state:
    st.session_state['is_double_line'] = False

if 'alternate_line' not in st.session_state:
    st.session_state['alternate_line'] = False

if 'current_line' not in st.session_state:
    st.session_state['current_line'] = 'A'

if 'current_end' not in st.session_state:
    st.session_state['current_end'] = 1

if 'is_buzzer_enabled' not in st.session_state:
    st.session_state['is_buzzer_enabled'] = True

## Previous State Trackers
if 'timer_active' not in st.session_state:
    st.session_state['timer_active'] = False

if 'last_setup_time' not in st.session_state:
    st.session_state['last_setup_time'] = st.session_state['setup_time']

if 'last_shooting_time' not in st.session_state:
    st.session_state['last_shooting_time'] = st.session_state['shooting_time']

if 'last_phase' not in st.session_state:
    st.session_state['last_phase'] = 'SETUP'

#-------------------#
#   Page Elements   #
#-------------------#

st.header("Timer Settings 🔧")

st.markdown(f"<span style='color: #c9b30c'>Don't use your browser's refresh/forward/back buttons while using this webapp. It will reset your session and clear all the settings.</span>", unsafe_allow_html=True)
st.markdown(f"<span style='color: #c9b30c'>Make sure you hit 'Apply' before leaving this page.</span>", unsafe_allow_html=True)

## Setup Two Column Layout
col1, col2 = st.columns(2)

## Column 1 Elements
num_practice_ends = col1.number_input("# Practice Ends (this currently does nothing)", min_value=0, value=st.session_state['num_practice_ends'], step=1, format="%d")
setup_time = col1.number_input("Setup Time (Seconds)", min_value=0, value=st.session_state['setup_time'], step=1, format="%d")

use_warning_color = col1.checkbox("Enable 'Warning' Color", value=st.session_state['use_warning_color'])
low_time_warning = col1.number_input("Time at which to display 'Warning' color:", max_value=st.session_state['shooting_time'], value=ceil(st.session_state['shooting_time']/3), step=1, format="%d")

is_double_line = col1.checkbox("Double Line", value=st.session_state['is_double_line'])

if is_double_line:
    alternate_line = col1.checkbox("Alternate A/B Start", value=st.session_state['alternate_line'])
else:
    alternate_line = False

is_buzzer_enabled = col1.checkbox("Enable Buzzer", value=st.session_state['is_buzzer_enabled'])

## Column 2 Elements
num_scoring_ends = col2.number_input("# Scoring Ends", min_value=0, value=st.session_state['num_scoring_ends'], step=1, format="%d")
shooting_time = col2.number_input("Shooting Time (Seconds)", min_value=0, value=st.session_state['shooting_time'], step=1, format="%d")

use_urgent_color = col2.checkbox("Enable 'Urgent' Color", value=st.session_state['use_urgent_color'])
low_time_urgent = col2.number_input("Time at which to display 'Urgent' color:", max_value=st.session_state['shooting_time'], value=ceil(st.session_state['shooting_time']/6), step=1, format="%d")

## "Apply" Button to Save Session State
if col1.button("Apply"):
    # Reset Main Defaults
    st.session_state['timer_active'] = False
    st.session_state['current_line'] = 'A'
    st.session_state['last_phase'] = 'SETUP'
    st.session_state['current_end'] = 1

    # Save Number of Ends
    st.session_state['num_practice_ends'] = num_practice_ends
    st.session_state['num_scoring_ends'] = num_scoring_ends

    # Save Time Settings
    st.session_state['setup_time'] = setup_time
    st.session_state['last_setup_time'] = setup_time
    st.session_state['shooting_time'] = shooting_time
    st.session_state['last_shooting_time'] = shooting_time

    # Save Flags
    st.session_state['is_double_line'] = is_double_line
    st.session_state['alternate_line'] = alternate_line

    st.session_state['use_warning_color'] = use_warning_color
    st.session_state['use_urgent_color'] = use_urgent_color

    st.session_state['low_time_warning'] = low_time_warning
    st.session_state['low_time_urgent'] = low_time_urgent

    st.session_state['is_buzzer_enabled'] = is_buzzer_enabled

    # Reload Page
    st.rerun()

#-------------------------------------------------#
###################### DEBUG ######################
#-------------------------------------------------#
#st.session_state