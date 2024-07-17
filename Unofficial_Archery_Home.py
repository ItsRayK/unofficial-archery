#-------------------#
#      Imports      #
#-------------------#

from pathlib import Path
import streamlit as st

#-------------------#
#       Setup       #
#-------------------#

THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / "style" / "style.css"
ASSETS = THIS_DIR / "assets"

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

if 'low_time_warning' not in st.session_state:
    st.session_state['low_time_warning'] = st.session_state['shooting_time']

if 'low_time_urgent' not in st.session_state:
    st.session_state['low_time_urgent'] = st.session_state['shooting_time']

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

# Display Header
RANGE_NAME = "Unofficial Archery"
st.header(f"Welcome to {RANGE_NAME}! 🎯", anchor=False)

# About Text
st.markdown('''
            ### About
            Unofficial Archery is exactly that! Your own unofficial archery range! ***Spin up a range wherever you are!*** (or rather, wherever you have an internet connection)
            
            *(Disclaimer: Yes, you can be an official range owner and still use this app to run your range if you want)*
            
            ### Features
            - **Range Commands**
                - **Commands**: On Line, Begin, Clear, Hold
                - **Buzzer**: Can be enabled for audible commands *(disabled by default)*
            - **Scoring Timer**
                - **Configurable**: Configure it to your liking under the "Timer Settings" page
                - **Buzzer Cues**: The buzzer sounds twice at the beginning for setup, once to begin shooting, and three times to signal the end *(can be disabled)*
                - **Double Line**: Enable the double line feature if your range is so popular that you don't have enough space *(disabled by default)*
            - **Countdown**
                - **Configurable**: Configure the time, title, and end text for whatever you need (i.e. event starting countdown, warm-up timer, etc.)
            
            ### Work In Progress
            Yup, this project is still a work in progress. If you encounter bugs, don't tell me about them, my ego is fragile (lol jk, ik there are bugs).

            There are still a handful of features missing that I'm working on.
            
            Here's the list:
            - ~Make it 'mobile' friendly (it's a disaster rn oops lol)~
            - Alternate 'A' and 'B' line for even and odd ends if double line is enabled
            - Add 'Practice End' functionality
            - Add button to skip the rest of the timer and go to the next scoring phase
            - Add keyboard shortcuts for range and timer controls
''')