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
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", initial_sidebar_state="collapsed")

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
if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

st.header("Timer Settings 🔧", anchor=False)

st.markdown(f"<span style='color: #c9b30c;'>Reminder: Don't use your browser's refresh/forward/back button.</span>", unsafe_allow_html=True)
st.markdown(f"<span style='color: #c9b30c;'>Make sure you hit 'Apply' before leaving this page.</span>", unsafe_allow_html=True)

## Setup Two Column Layout
col1, col2 = st.columns(2)

## Column 1 Elements
num_practice_ends = col1.number_input("# Practice Ends (this currently does nothing)", min_value=0, value=st.session_state['num_practice_ends'], step=1, format="%d")
num_scoring_ends = col1.number_input("# Scoring Ends", min_value=0, value=st.session_state['num_scoring_ends'], step=1, format="%d")
setup_time = col1.number_input("Setup Time (Seconds)", min_value=0, value=st.session_state['setup_time'], step=1, format="%d")
shooting_time = col1.number_input("Shooting Time (Seconds)", min_value=0, value=st.session_state['shooting_time'], step=1, format="%d")

## Column 2 Elements
low_time_warning = col2.number_input("Time at which to display 'Warning' color:", max_value=st.session_state['shooting_time'], value=ceil(st.session_state['shooting_time']/3), step=1, format="%d")
low_time_urgent = col2.number_input("Time at which to display 'Urgent' color:", max_value=st.session_state['shooting_time'], value=ceil(st.session_state['shooting_time']/6), step=1, format="%d")

use_warning_color = col2.checkbox("Enable 'Warning' Color", value=st.session_state['use_warning_color'])
use_urgent_color = col2.checkbox("Enable 'Urgent' Color", value=st.session_state['use_urgent_color'])

is_double_line = col2.checkbox("Double Line", value=st.session_state['is_double_line'])

if is_double_line:
    alternate_line = col2.checkbox("Alternate A/B Start", value=st.session_state['alternate_line'])
else:
    alternate_line = False

is_buzzer_enabled = col2.checkbox("Enable Buzzer", value=st.session_state['is_buzzer_enabled'])

col2.divider()

## Nested Columns
col2_1, col2_2 = col2.columns(2)

## "Apply" Button to Save Session State
if col2_1.button("Apply", use_container_width=True):
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

if col2_2.button("Apply & Open Timer", use_container_width=True):
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

    st.switch_page("./pages/Timer.py")

col2.divider()

if col2.button("Don't Save & Open Timer", use_container_width=True):
    st.switch_page("./pages/Timer.py")

#-------------------------------------------------#
###################### DEBUG ######################
#-------------------------------------------------#
#st.session_state