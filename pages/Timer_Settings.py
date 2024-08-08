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

if 'is_practice_end' not in st.session_state:
    if st.session_state['num_practice_ends'] > 0:
        st.session_state['is_practice_end'] = True
    else:
        st.session_state['is_practice_end'] = False

if 'num_scoring_ends' not in st.session_state:
    st.session_state['num_scoring_ends'] = 10

if 'is_double_line' not in st.session_state:
    st.session_state['is_double_line'] = False

if 'alternate_line' not in st.session_state:
    st.session_state['alternate_line'] = True

if 'current_line' not in st.session_state:
    st.session_state['current_line'] = 'A'

if 'current_end' not in st.session_state:
    st.session_state['current_end'] = 1

if 'current_practice_end' not in st.session_state:
    st.session_state['current_practice_end'] = 1

if 'is_buzzer_enabled' not in st.session_state:
    st.session_state['is_buzzer_enabled'] = True

if 'buzzer_style' not in st.session_state:
    st.session_state['buzzer_style'] = 'DEFAULT'

## Previous State Trackers
if 'timer_active' not in st.session_state:
    st.session_state['timer_active'] = False

if 'last_setup_time' not in st.session_state:
    st.session_state['last_setup_time'] = st.session_state['setup_time']

if 'last_shooting_time' not in st.session_state:
    st.session_state['last_shooting_time'] = st.session_state['shooting_time']

if 'last_phase' not in st.session_state:
    st.session_state['last_phase'] = 'ON LINE'

#-------------------#
#   Page Elements   #
#-------------------#
if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

st.header("Timer Settings 🔧", anchor=False)

st.markdown(f"<span style='color: #c9b30c;'>Reminder: Don't use your browser's refresh/forward/back button.</span>", unsafe_allow_html=True)
st.markdown(f"<span style='color: #c9b30c;'>Make sure you hit 'Apply' before leaving this page.</span>", unsafe_allow_html=True)

col1_1, col1_2 = st.columns(2)

num_scoring_ends = col1_1.number_input("# Scoring Ends", min_value=0, value=st.session_state['num_scoring_ends'], step=1, format="%d")
num_practice_ends = col1_2.number_input("# Practice Ends", min_value=0, value=st.session_state['num_practice_ends'], step=1, format="%d")

col2_1, col2_2 = st.columns(2)

setup_time = col2_1.number_input("Setup Time (Seconds)", min_value=0, value=st.session_state['setup_time'], step=1, format="%d")
shooting_time = col2_2.number_input("Shooting Time (Seconds)", min_value=0, value=st.session_state['shooting_time'], step=1, format="%d")

use_warning_color = st.checkbox("Enable 'Warning' Color", value=st.session_state['use_warning_color'])
if use_warning_color:
    low_time_warning = st.number_input("Time at which to display 'Warning' color:", max_value=st.session_state['shooting_time'], value=min(st.session_state['low_time_warning'],st.session_state['shooting_time']), step=1, format="%d")
else:
    low_time_warning = ceil(st.session_state['shooting_time']/3)

use_urgent_color = st.checkbox("Enable 'Urgent' Color", value=st.session_state['use_urgent_color'])
if use_urgent_color:
    low_time_urgent = st.number_input("Time at which to display 'Urgent' color:", max_value=st.session_state['shooting_time'], value=min(st.session_state['low_time_urgent'],st.session_state['shooting_time']), step=1, format="%d")
else:
    low_time_urgent = ceil(st.session_state['shooting_time']/6)

is_double_line = st.checkbox("Double Line", value=st.session_state['is_double_line'])

if is_double_line:
    alternate_line = st.checkbox("Alternate A/B Start", value=st.session_state['alternate_line'])
else:
    alternate_line = False

is_buzzer_enabled = st.checkbox("Enable Buzzer", value=st.session_state['is_buzzer_enabled'])

if is_buzzer_enabled:
    buzzer_style = st.selectbox(
    "Buzzer Style:",
    ("DEFAULT", "SOFT", "HARSH")
)

st.divider()

col6_1, col6_2 = st.columns(2)

## "Apply" Button to Save Session State
if col6_1.button("Apply", use_container_width=True):
    # Reset Main Defaults
    st.session_state['timer_active'] = False
    st.session_state['current_line'] = 'A'
    st.session_state['last_phase'] = 'ON LINE'
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
    st.session_state['buzzer_style'] = buzzer_style
    # Reload Page
    st.rerun()

if col6_2.button("Apply & Open Timer", use_container_width=True):
    # Reset Main Defaults
    st.session_state['timer_active'] = False
    st.session_state['current_line'] = 'A'
    st.session_state['last_phase'] = 'ON LINE'
    st.session_state['current_end'] = 1
    st.session_state['current_practice_end'] = 1

    # Save Number of Ends
    st.session_state['num_practice_ends'] = num_practice_ends
    st.session_state['num_scoring_ends'] = num_scoring_ends

    # Save Time Settings
    st.session_state['setup_time'] = setup_time
    st.session_state['last_setup_time'] = setup_time
    st.session_state['shooting_time'] = shooting_time
    st.session_state['last_shooting_time'] = shooting_time

    # Save Flags
    st.session_state['is_practice_end'] = num_practice_ends > 0

    st.session_state['is_double_line'] = is_double_line
    st.session_state['alternate_line'] = alternate_line

    st.session_state['use_warning_color'] = use_warning_color
    st.session_state['use_urgent_color'] = use_urgent_color

    st.session_state['low_time_warning'] = low_time_warning
    st.session_state['low_time_urgent'] = low_time_urgent

    st.session_state['is_buzzer_enabled'] = is_buzzer_enabled
    st.session_state['buzzer_style'] = buzzer_style

    st.switch_page("./pages/Timer.py")

col6_1.divider()

if col6_1.button("Don't Save & Open Timer", use_container_width=True):
    st.switch_page("./pages/Timer.py")

#-------------------------------------------------#
###################### DEBUG ######################
#-------------------------------------------------#
#st.session_state