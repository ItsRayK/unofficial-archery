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

### Page Configuration
st.set_page_config(page_title="Unofficial Archery", page_icon="🎯", initial_sidebar_state="collapsed", layout="wide")

### Apply Custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#-------------------#
#   Page Elements   #
#-------------------#

if st.button("🎯 Home"):
    st.switch_page("./Unofficial_Archery_Home.py")

col1, col2, col3 = st.columns([0.2,0.6,0.2])

# Display Header
col2.header(f"About 🎯", anchor=False)

# About Text
col2.markdown('''
            Unofficial Archery is exactly that! Your own unofficial archery range! ***Spin up a range wherever you are!*** (or rather, wherever you have an internet connection)
            
            *(Disclaimer: Yes, you can be an official range owner and still use this app to run your range if you want)*
            
            ### Features
            - **Range Commands**
                - **Commands**: On Line, Begin, Clear, Hold
                - **Buzzer**: Can be enabled for audible commands *(disabled by default)*
                - **Hotkeys**: Control the range with just a keyboard *(Keys for the range: 1 = ON LINE | 2 = BEGIN | 3 = SHOOT | 4 = HOLD)*
            - **Scoring Timer**
                - **Configurable**: Configure it to your liking under the "Timer Settings" page
                - **Buzzer Cues**: The buzzer sounds twice at the beginning for setup, once to begin shooting, and three times to signal the end *(can be disabled)*
                - **Double Line**: Enable the double line feature if your range is so popular that you don't have enough space *(disabled by default)*
                - **Hotkeys**: Start/Stop the timer with just a keyboard *(Keys for timer: S = Start/Stop)*
            - **Countdown**
                - **Configurable**: Configure the time, title, and end text for whatever you need (i.e. event starting countdown, warm-up timer, etc.)
                - **Hotkeys**: Start/Stop the timer with just a keyboard *(Keys for timer: S = Start/Stop)*
            
            ### Work In Progress
            Yup, this project is still a work in progress. If you encounter bugs, don't tell me about them, my ego is fragile (lol jk, ik there are bugs).

            There are still a handful of features missing that I'm working on.
            
            Here's the list:
            - ~Make it 'mobile' friendly (it's a disaster rn oops lol)~
            - ~Alternate 'A' and 'B' line for even and odd ends if double line is enabled~
            - Add 'Practice End' functionality
            - ~Add button to skip the rest of the timer and go to the next scoring phase~
            - ~Add keyboard shortcuts for range and timer controls~
''')